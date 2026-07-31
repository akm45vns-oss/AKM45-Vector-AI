"""
Company repository — database operations for Company model.
"""

import uuid
from typing import Optional, Sequence

import structlog
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate

logger = structlog.get_logger(__name__)


class CompanyRepository:
    """Data access layer for the Company model."""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def get_by_id(self, company_id: uuid.UUID) -> Optional[Company]:
        """Fetch company by UUID."""
        result = await self._db.execute(
            select(Company).where(Company.id == company_id)
        )
        return result.scalar_one_or_none()

    async def list_companies(
        self, *, skip: int = 0, limit: int = 20, search: Optional[str] = None
    ) -> Sequence[Company]:
        """List companies with optional search and pagination."""
        query = select(Company).order_by(Company.name.asc())
        if search:
            query = query.where(Company.name.ilike(f"%{search}%"))
        query = query.offset(skip).limit(limit)
        result = await self._db.execute(query)
        return result.scalars().all()

    async def create(self, company_in: CompanyCreate, created_by_id: uuid.UUID) -> Company:
        """Create a new company record."""
        company = Company(
            name=company_in.name.strip(),
            website=company_in.website,
            industry=company_in.industry,
            size=company_in.size,
            logo_url=company_in.logo_url,
            description=company_in.description,
            created_by_id=created_by_id,
        )
        self._db.add(company)
        await self._db.flush()
        await self._db.refresh(company)
        logger.info("Company created", company_id=str(company.id), name=company.name)
        return company

    async def update(self, company_id: uuid.UUID, company_in: CompanyUpdate) -> Optional[Company]:
        """Update an existing company."""
        values = company_in.model_dump(exclude_unset=True)
        if not values:
            return await self.get_by_id(company_id)

        await self._db.execute(
            update(Company).where(Company.id == company_id).values(**values)
        )
        return await self.get_by_id(company_id)

    async def delete(self, company_id: uuid.UUID) -> bool:
        """Delete a company by ID."""
        result = await self._db.execute(
            delete(Company).where(Company.id == company_id)
        )
        return result.rowcount > 0
