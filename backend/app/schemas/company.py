"""
Company Pydantic schemas.
"""

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, HttpUrl


class CompanyBase(BaseModel):
    name: str
    website: str | None = None
    industry: str | None = None
    size: str | None = None
    logo_url: str | None = None
    description: str | None = None


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: str | None = None
    website: str | None = None
    industry: str | None = None
    size: str | None = None
    logo_url: str | None = None
    description: str | None = None


class CompanyResponse(CompanyBase):
    id: UUID
    created_by_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
