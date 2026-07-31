"""
Jobs API endpoints.
"""

import uuid
from typing import Optional, Sequence

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import RecruiterUser, get_db
from app.models.job import EmploymentType, JobStatus
from app.models.user import User
from app.schemas.job import JobCreate, JobListFilter, JobResponse, JobUpdate
from app.services.job_service import JobService

router = APIRouter()


@router.post("", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
    job_in: JobCreate,
    current_user: User = Depends(RecruiterUser),
    db: AsyncSession = Depends(get_db),
) -> JobResponse:
    """Create a new job posting (recruiter or admin)."""
    service = JobService(db)
    return await service.create_job(job_in, current_user)


@router.get("", response_model=Sequence[JobResponse])
async def list_jobs(
    company_id: Optional[uuid.UUID] = Query(None),
    status_filter: Optional[JobStatus] = Query(None, alias="status"),
    employment_type: Optional[EmploymentType] = Query(None),
    location: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> Sequence[JobResponse]:
    """List jobs with pagination and filter criteria."""
    filters = JobListFilter(
        company_id=company_id,
        status=status_filter,
        employment_type=employment_type,
        location=location,
        search=search,
        skip=skip,
        limit=limit,
    )
    service = JobService(db)
    return await service.list_jobs(filters)


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> JobResponse:
    """Get job details by ID."""
    service = JobService(db)
    return await service.get_job(job_id)


@router.patch("/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: uuid.UUID,
    job_in: JobUpdate,
    current_user: User = Depends(RecruiterUser),
    db: AsyncSession = Depends(get_db),
) -> JobResponse:
    """Update job posting."""
    service = JobService(db)
    return await service.update_job(job_id, job_in, current_user)


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(
    job_id: uuid.UUID,
    current_user: User = Depends(RecruiterUser),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete job posting."""
    service = JobService(db)
    await service.delete_job(job_id, current_user)
