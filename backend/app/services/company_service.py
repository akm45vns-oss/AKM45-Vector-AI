"""
Company service — business logic for company management.
"""

import uuid
from typing import Optional, Sequence

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.company_repository import CompanyRepository
from app.schemas.company import CompanyCreate, CompanyResponse, CompanyUpdate


class CompanyService:
    """Business logic for companies."""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db
        self._repo = CompanyRepository(db)

    async def create_company(self, company_in: CompanyCreate, user: User) -> CompanyResponse:
        """Create a company (recruiters/admins only)."""
        company = await self._repo.create(company_in, created_by_id=user.id)
        await self._db.commit()
        return CompanyResponse.model_validate(company)

    async def get_company(self, company_id: uuid.UUID) -> CompanyResponse:
        """Get company details by ID."""
        company = await self._repo.get_by_id(company_id)
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company not found",
            )
        return CompanyResponse.model_validate(company)

    async def list_companies(
        self, *, skip: int = 0, limit: int = 20, search: Optional[str] = None
    ) -> Sequence[CompanyResponse]:
        """List companies with optional search and pagination."""
        companies = await self._repo.list_companies(skip=skip, limit=limit, search=search)
        return [CompanyResponse.model_validate(c) for c in companies]

    async def update_company(
        self, company_id: uuid.UUID, company_in: CompanyUpdate, user: User
    ) -> CompanyResponse:
        """Update company profile."""
        company = await self._repo.get_by_id(company_id)
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company not found",
            )
        if user.role != "admin" and company.created_by_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to edit this company",
            )

        updated = await self._repo.update(company_id, company_in)
        await self._db.commit()
        return CompanyResponse.model_validate(updated)

    async def delete_company(self, company_id: uuid.UUID, user: User) -> None:
        """Delete company."""
        company = await self._repo.get_by_id(company_id)
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company not found",
            )
        if user.role != "admin" and company.created_by_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this company",
            )

        await self._repo.delete(company_id)
        await self._db.commit()
