"""
Applications API endpoints.
"""

import uuid
from typing import Optional, Sequence

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import (
    CandidateUser,
    RecruiterUser,
    get_current_user,
    get_db,
)
from app.models.user import User
from app.schemas.application import (
    ApplicationCreate,
    ApplicationResponse,
    ApplicationStatusUpdate,
)
from app.services.application_service import ApplicationService

router = APIRouter()


@router.post("", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
async def apply_to_job(
    app_in: ApplicationCreate,
    current_user: User = Depends(CandidateUser),
    db: AsyncSession = Depends(get_db),
) -> ApplicationResponse:
    """Submit application for a job (candidate only)."""
    service = ApplicationService(db)
    return await service.apply_to_job(app_in, current_user)


@router.get("", response_model=Sequence[ApplicationResponse])
async def list_applications(
    job_id: Optional[uuid.UUID] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Sequence[ApplicationResponse]:
    """List applications (candidates see their own; recruiters see all or filter by job_id)."""
    service = ApplicationService(db)
    return await service.list_applications(
        current_user, job_id=job_id, skip=skip, limit=limit
    )


@router.get("/{application_id}", response_model=ApplicationResponse)
async def get_application(
    application_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ApplicationResponse:
    """Get single application details."""
    service = ApplicationService(db)
    return await service.get_application(application_id, current_user)


@router.patch("/{application_id}/status", response_model=ApplicationResponse)
async def update_application_status(
    application_id: uuid.UUID,
    status_in: ApplicationStatusUpdate,
    current_user: User = Depends(RecruiterUser),
    db: AsyncSession = Depends(get_db),
) -> ApplicationResponse:
    """Update application status (recruiter or admin)."""
    service = ApplicationService(db)
    return await service.update_status(application_id, status_in, current_user)
