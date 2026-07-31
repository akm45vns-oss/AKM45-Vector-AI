"""
Job Pydantic schemas.
"""

from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.job import EmploymentType, JobStatus
from app.schemas.company import CompanyResponse


class SkillRequirement(BaseModel):
    skill_name: str
    is_required: bool = True
    weight: float = 1.0


class JobBase(BaseModel):
    title: str
    description: str
    requirements: str | None = None
    location: str | None = None
    employment_type: EmploymentType = EmploymentType.FULL_TIME
    status: JobStatus = JobStatus.DRAFT
    min_salary: Decimal | None = None
    max_salary: Decimal | None = None
    currency: str = "USD"
    experience_years_required: int | None = 0


class JobCreate(JobBase):
    company_id: UUID
    skills: List[SkillRequirement] = []


class JobUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    requirements: str | None = None
    location: str | None = None
    employment_type: EmploymentType | None = None
    status: JobStatus | None = None
    min_salary: Decimal | None = None
    max_salary: Decimal | None = None
    currency: str | None = None
    experience_years_required: int | None = None
    skills: Optional[List[SkillRequirement]] = None


class JobResponse(JobBase):
    id: UUID
    company_id: UUID
    recruiter_id: UUID
    created_at: datetime
    updated_at: datetime
    company: Optional[CompanyResponse] = None

    model_config = ConfigDict(from_attributes=True)


class JobListFilter(BaseModel):
    company_id: UUID | None = None
    status: JobStatus | None = None
    employment_type: EmploymentType | None = None
    location: str | None = None
    search: str | None = None
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=20, ge=1, le=100)
