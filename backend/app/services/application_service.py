"""
Application service — business logic for job applications.
"""

import uuid
from typing import Optional, Sequence

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.application_repository import ApplicationRepository
from app.repositories.job_repository import JobRepository
from app.schemas.application import (
    ApplicationCreate,
    ApplicationResponse,
    ApplicationStatusUpdate,
)


class ApplicationService:
    """Business logic for job applications."""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db
        self._repo = ApplicationRepository(db)
        self._job_repo = JobRepository(db)

    async def apply_to_job(
        self, app_in: ApplicationCreate, candidate: User
    ) -> ApplicationResponse:
        """Submit job application."""
        job = await self._job_repo.get_by_id(app_in.job_id)
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Target job posting not found",
            )

        # Check if already applied
        existing = await self._repo.list_applications(
            candidate_id=candidate.id, job_id=app_in.job_id
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already applied to this job posting",
            )

        application = await self._repo.create(app_in, candidate_id=candidate.id)
        await self._db.commit()
        return ApplicationResponse.model_validate(application)

    async def get_application(
        self, application_id: uuid.UUID, user: User
    ) -> ApplicationResponse:
        """Get application details with permission check."""
        app = await self._repo.get_by_id(application_id)
        if not app:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found",
            )

        # Candidate can view their own application; Recruiter/Admin can view any
        if user.role == "candidate" and app.candidate_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this application",
            )

        return ApplicationResponse.model_validate(app)

    async def list_applications(
        self,
        user: User,
        *,
        job_id: Optional[uuid.UUID] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> Sequence[ApplicationResponse]:
        """List applications for candidate or recruiter."""
        candidate_id = user.id if user.role == "candidate" else None
        apps = await self._repo.list_applications(
            candidate_id=candidate_id, job_id=job_id, skip=skip, limit=limit
        )
        return [ApplicationResponse.model_validate(a) for a in apps]

    async def update_status(
        self,
        application_id: uuid.UUID,
        status_in: ApplicationStatusUpdate,
        user: User,
    ) -> ApplicationResponse:
        """Update application status (recruiters/admins only)."""
        app = await self._repo.get_by_id(application_id)
        if not app:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Application not found",
            )

        if user.role == "candidate":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Candidates cannot alter application status",
            )

        updated = await self._repo.update_status(application_id, status_in)
        await self._db.commit()
        return ApplicationResponse.model_validate(updated)
