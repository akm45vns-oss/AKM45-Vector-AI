"""
Skill and Skill Association SQLAlchemy models.
"""

import uuid
from typing import TYPE_CHECKING, List

from sqlalchemy import (
    Boolean,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.engine import Base

if TYPE_CHECKING:
    from app.models.job import Job
    from app.models.resume import Resume


class Skill(Base):
    """
    Skill reference dictionary model.
    """

    __tablename__ = "skills"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)

    def __repr__(self) -> str:
        return f"<Skill id={self.id} name={self.name!r}>"


class ResumeSkill(Base):
    """
    Association table between Resume and Skill.
    """

    __tablename__ = "resume_skills"

    resume_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("resumes.id", ondelete="CASCADE"),
        primary_key=True,
    )
    skill_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("skills.id", ondelete="CASCADE"),
        primary_key=True,
    )
    years_experience: Mapped[float | None] = mapped_column(Float, nullable=True)
    proficiency_level: Mapped[str | None] = mapped_column(String(50), nullable=True)  # e.g., "Beginner", "Intermediate", "Expert"

    # Relationships
    resume: Mapped["Resume"] = relationship("Resume", back_populates="resume_skills")
    skill: Mapped["Skill"] = relationship("Skill")


class JobSkill(Base):
    """
    Association table between Job and Skill.
    """

    __tablename__ = "job_skills"

    job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("jobs.id", ondelete="CASCADE"),
        primary_key=True,
    )
    skill_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("skills.id", ondelete="CASCADE"),
        primary_key=True,
    )
    is_required: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    weight: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)

    # Relationships
    job: Mapped["Job"] = relationship("Job", back_populates="job_skills")
    skill: Mapped["Skill"] = relationship("Skill")
