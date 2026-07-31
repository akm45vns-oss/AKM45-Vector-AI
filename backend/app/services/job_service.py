"""
Job service — business logic for job postings.
"""

import uuid
from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.company_repository import CompanyRepository
from app.repositories.job_repository import JobRepository
from app.schemas.job import JobCreate, JobListFilter, JobResponse, JobUpdate


class JobService:
    """Business logic for jobs."""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db
        self._repo = JobRepository(db)
        self._company_repo = CompanyRepository(db)

    async def create_job(self, job_in: JobCreate, user: User) -> JobResponse:
        """Create a job posting."""
        company = await self._company_repo.get_by_id(job_in.company_id)
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Target company does not exist",
            )

        job = await self._repo.create(job_in, recruiter_id=user.id)
        await self._db.commit()
        return JobResponse.model_validate(job)

    async def get_job(self, job_id: uuid.UUID) -> JobResponse:
        """Get job by ID."""
        job = await self._repo.get_by_id(job_id)
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job posting not found",
            )
        return JobResponse.model_validate(job)

    async def list_jobs(self, filters: JobListFilter) -> Sequence[JobResponse]:
        """List jobs with filters."""
        jobs = await self._repo.list_jobs(filters)
        return [JobResponse.model_validate(j) for j in jobs]

    async def update_job(
        self, job_id: uuid.UUID, job_in: JobUpdate, user: User
    ) -> JobResponse:
        """Update job details."""
        job = await self._repo.get_by_id(job_id)
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job posting not found",
            )
        if user.role != "admin" and job.recruiter_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to modify this job posting",
            )

        updated = await self._repo.update(job_id, job_in)
        await self._db.commit()
        return JobResponse.model_validate(updated)

    async def delete_job(self, job_id: uuid.UUID, user: User) -> None:
        """Delete job posting."""
        job = await self._repo.get_by_id(job_id)
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job posting not found",
            )
        if user.role != "admin" and job.recruiter_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this job posting",
            )

        await self._repo.delete(job_id)
        await self._db.commit()
