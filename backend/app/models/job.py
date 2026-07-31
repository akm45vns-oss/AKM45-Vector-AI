"""
Job SQLAlchemy model.
"""

import uuid
from datetime import datetime
from enum import Enum as PyEnum
from typing import TYPE_CHECKING, List

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.engine import Base

if TYPE_CHECKING:
    from app.models.application import Application
    from app.models.company import Company
    from app.models.skill import JobSkill
    from app.models.user import User


class JobStatus(str, PyEnum):
    """Job status options."""
    DRAFT = "draft"
    PUBLISHED = "published"
    CLOSED = "closed"
    ARCHIVED = "archived"


class EmploymentType(str, PyEnum):
    """Employment type options."""
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    REMOTE = "remote"
    INTERNSHIP = "internship"


class Job(Base):
    """
    Job posting model.
    """

    __tablename__ = "jobs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    company_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    recruiter_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    requirements: Mapped[str | None] = mapped_column(Text, nullable=True)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    
    employment_type: Mapped[EmploymentType] = mapped_column(
        Enum(EmploymentType, name="employmenttype", create_constraint=True),
        nullable=False,
        default=EmploymentType.FULL_TIME,
    )
    status: Mapped[JobStatus] = mapped_column(
        Enum(JobStatus, name="jobstatus", create_constraint=True),
        nullable=False,
        default=JobStatus.DRAFT,
        index=True,
    )
    
    min_salary: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    max_salary: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    experience_years_required: Mapped[int | None] = mapped_column(Integer, default=0, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
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
    company: Mapped["Company"] = relationship("Company", back_populates="jobs")
    recruiter: Mapped["User"] = relationship("User", backref="posted_jobs")
    job_skills: Mapped[List["JobSkill"]] = relationship("JobSkill", back_populates="job", cascade="all, delete-orphan")
    applications: Mapped[List["Application"]] = relationship("Application", back_populates="job", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Job id={self.id} title={self.title!r} status={self.status}>"
