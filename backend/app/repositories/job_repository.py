"""
Job repository — database operations for Job model.
"""

import uuid
from typing import Optional, Sequence

import structlog
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.job import Job, JobStatus
from app.models.skill import Skill, JobSkill
from app.schemas.job import JobCreate, JobListFilter, JobUpdate

logger = structlog.get_logger(__name__)


class JobRepository:
    """Data access layer for the Job model."""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def get_by_id(self, job_id: uuid.UUID) -> Optional[Job]:
        """Fetch job by UUID with eager loaded company."""
        result = await self._db.execute(
            select(Job)
            .options(selectinload(Job.company), selectinload(Job.job_skills).selectinload(JobSkill.skill))
            .where(Job.id == job_id)
        )
        return result.scalar_one_or_none()

    async def list_jobs(self, filters: JobListFilter) -> Sequence[Job]:
        """List jobs with filtering and pagination."""
        query = select(Job).options(selectinload(Job.company)).order_by(Job.created_at.desc())

        if filters.company_id:
            query = query.where(Job.company_id == filters.company_id)
        if filters.status:
            query = query.where(Job.status == filters.status)
        if filters.employment_type:
            query = query.where(Job.employment_type == filters.employment_type)
        if filters.location:
            query = query.where(Job.location.ilike(f"%{filters.location}%"))
        if filters.search:
            query = query.where(
                (Job.title.ilike(f"%{filters.search}%")) |
                (Job.description.ilike(f"%{filters.search}%"))
            )

        query = query.offset(filters.skip).limit(filters.limit)
        result = await self._db.execute(query)
        return result.scalars().all()

    async def create(self, job_in: JobCreate, recruiter_id: uuid.UUID) -> Job:
        """Create a new job posting with skill requirements."""
        job = Job(
            company_id=job_in.company_id,
            recruiter_id=recruiter_id,
            title=job_in.title.strip(),
            description=job_in.description,
            requirements=job_in.requirements,
            location=job_in.location,
            employment_type=job_in.employment_type,
            status=job_in.status,
            min_salary=job_in.min_salary,
            max_salary=job_in.max_salary,
            currency=job_in.currency,
            experience_years_required=job_in.experience_years_required,
        )
        self._db.add(job)
        await self._db.flush()

        # Handle skill associations if provided
        for item in job_in.skills:
            # Find or create skill
            normalized_name = item.skill_name.lower().strip()
            skill_res = await self._db.execute(select(Skill).where(Skill.name == normalized_name))
            skill = skill_res.scalar_one_or_none()
            if not skill:
                skill = Skill(name=normalized_name)
                self._db.add(skill)
                await self._db.flush()

            job_skill = JobSkill(
                job_id=job.id,
                skill_id=skill.id,
                is_required=item.is_required,
                weight=item.weight,
            )
            self._db.add(job_skill)

        await self._db.flush()
        await self._db.refresh(job)
        logger.info("Job created", job_id=str(job.id), title=job.title)
        return await self.get_by_id(job.id)  # return with relationships loaded

    async def update(self, job_id: uuid.UUID, job_in: JobUpdate) -> Optional[Job]:
        """Update an existing job posting."""
        values = job_in.model_dump(exclude_unset=True, exclude={"skills"})
        if values:
            await self._db.execute(
                update(Job).where(Job.id == job_id).values(**values)
            )

        if job_in.skills is not None:
            # Clear old skill associations
            await self._db.execute(delete(JobSkill).where(JobSkill.job_id == job_id))
            for item in job_in.skills:
                normalized_name = item.skill_name.lower().strip()
                skill_res = await self._db.execute(select(Skill).where(Skill.name == normalized_name))
                skill = skill_res.scalar_one_or_none()
                if not skill:
                    skill = Skill(name=normalized_name)
                    self._db.add(skill)
                    await self._db.flush()

                job_skill = JobSkill(
                    job_id=job_id,
                    skill_id=skill.id,
                    is_required=item.is_required,
                    weight=item.weight,
                )
                self._db.add(job_skill)

        return await self.get_by_id(job_id)

    async def delete(self, job_id: uuid.UUID) -> bool:
        """Delete a job posting."""
        result = await self._db.execute(
            delete(Job).where(Job.id == job_id)
        )
        return result.rowcount > 0
