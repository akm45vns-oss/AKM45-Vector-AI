"""
Application Pydantic schemas.
"""

from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.application import ApplicationStatus
from app.schemas.job import JobResponse


class ApplicationCreate(BaseModel):
    job_id: UUID
    resume_id: UUID


class ApplicationStatusUpdate(BaseModel):
    status: ApplicationStatus
    notes: str | None = None


class ApplicationResponse(BaseModel):
    id: UUID
    job_id: UUID
    resume_id: UUID
    candidate_id: UUID
    status: ApplicationStatus
    match_score: float | None = None
    match_breakdown: Dict[str, Any] | None = None
    llm_feedback: str | None = None
    notes: str | None = None
    applied_at: datetime
    updated_at: datetime
    job: Optional[JobResponse] = None

    model_config = ConfigDict(from_attributes=True)
