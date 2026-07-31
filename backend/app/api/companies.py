"""
Companies API endpoints.
"""

import uuid
from typing import Optional, Sequence

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import RecruiterUser, get_current_user, get_db
from app.models.user import User
from app.schemas.company import CompanyCreate, CompanyResponse, CompanyUpdate
from app.services.company_service import CompanyService

router = APIRouter()


@router.post("", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
async def create_company(
    company_in: CompanyCreate,
    current_user: User = Depends(RecruiterUser),
    db: AsyncSession = Depends(get_db),

) -> CompanyResponse:
    """Create a company record (recruiter or admin)."""
    service = CompanyService(db)
    return await service.create_company(company_in, current_user)


@router.get("", response_model=Sequence[CompanyResponse])
async def list_companies(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
) -> Sequence[CompanyResponse]:
    """List companies with pagination and optional search."""
    service = CompanyService(db)
    return await service.list_companies(skip=skip, limit=limit, search=search)


@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(
    company_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> CompanyResponse:
    """Get company details by ID."""
    service = CompanyService(db)
    return await service.get_company(company_id)


@router.patch("/{company_id}", response_model=CompanyResponse)
async def update_company(
    company_id: uuid.UUID,
    company_in: CompanyUpdate,
    current_user: User = Depends(RecruiterUser),
    db: AsyncSession = Depends(get_db),
) -> CompanyResponse:
    """Update company details."""
    service = CompanyService(db)
    return await service.update_company(company_id, company_in, current_user)


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(
    company_id: uuid.UUID,
    current_user: User = Depends(RecruiterUser),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete company."""
    service = CompanyService(db)
    await service.delete_company(company_id, current_user)
