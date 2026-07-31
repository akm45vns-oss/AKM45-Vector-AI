"""
Application repository — database operations for Application model.
"""

import uuid
from typing import Optional, Sequence

import structlog
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.application import Application, ApplicationStatus
from app.schemas.application import ApplicationCreate, ApplicationStatusUpdate

logger = structlog.get_logger(__name__)


class ApplicationRepository:
    """Data access layer for Application model."""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def get_by_id(self, application_id: uuid.UUID) -> Optional[Application]:
        """Fetch application by ID with eager loaded job."""
        result = await self._db.execute(
            select(Application)
            .options(selectinload(Application.job))
            .where(Application.id == application_id)
        )
        return result.scalar_one_or_none()

    async def list_applications(
        self,
        *,
        candidate_id: Optional[uuid.UUID] = None,
        job_id: Optional[uuid.UUID] = None,
        status: Optional[ApplicationStatus] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> Sequence[Application]:
        """List applications with optional candidate/job filters."""
        query = (
            select(Application)
            .options(selectinload(Application.job))
            .order_by(Application.applied_at.desc())
        )

        if candidate_id:
            query = query.where(Application.candidate_id == candidate_id)
        if job_id:
            query = query.where(Application.job_id == job_id)
        if status:
            query = query.where(Application.status == status)

        query = query.offset(skip).limit(limit)
        result = await self._db.execute(query)
        return result.scalars().all()

    async def create(self, app_in: ApplicationCreate, candidate_id: uuid.UUID) -> Application:
        """Create a new job application."""
        application = Application(
            job_id=app_in.job_id,
            resume_id=app_in.resume_id,
            candidate_id=candidate_id,
            status=ApplicationStatus.APPLIED,
        )
        self._db.add(application)
        await self._db.flush()
        await self._db.refresh(application)
        logger.info("Application submitted", application_id=str(application.id), job_id=str(app_in.job_id))
        return await self.get_by_id(application.id)

    async def update_status(
        self, application_id: uuid.UUID, status_in: ApplicationStatusUpdate
    ) -> Optional[Application]:
        """Update status and notes of an application."""
        values: dict = {"status": status_in.status}
        if status_in.notes is not None:
            values["notes"] = status_in.notes

        await self._db.execute(
            update(Application)
            .where(Application.id == application_id)
            .values(**values)
        )
        return await self.get_by_id(application_id)
