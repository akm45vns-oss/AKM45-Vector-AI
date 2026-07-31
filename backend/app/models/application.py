"""
Application SQLAlchemy model.
"""

import uuid
from datetime import datetime
from enum import Enum as PyEnum
from typing import TYPE_CHECKING, Any, Dict

from sqlalchemy import (
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.engine import Base

if TYPE_CHECKING:
    from app.models.job import Job
    from app.models.resume import Resume
    from app.models.user import User


class ApplicationStatus(str, PyEnum):
    """Application status options."""
    APPLIED = "applied"
    SCREENING = "screening"
    SHORTLISTED = "shortlisted"
    INTERVIEWING = "interviewing"
    OFFERED = "offered"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class Application(Base):
    """
    Job Application model connecting candidate resume to job posting.
    """

    __tablename__ = "applications"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    resume_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("resumes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    candidate_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    
    status: Mapped[ApplicationStatus] = mapped_column(
        Enum(ApplicationStatus, name="applicationstatus", create_constraint=True),
        nullable=False,
        default=ApplicationStatus.APPLIED,
        index=True,
    )
    match_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    match_breakdown: Mapped[Dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    llm_feedback: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    applied_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    job: Mapped["Job"] = relationship("Job", back_populates="applications")
    resume: Mapped["Resume"] = relationship("Resume", back_populates="applications")
    candidate: Mapped["User"] = relationship("User", backref="applications")

    def __repr__(self) -> str:
        return f"<Application id={self.id} job_id={self.job_id} candidate_id={self.candidate_id} status={self.status}>"
