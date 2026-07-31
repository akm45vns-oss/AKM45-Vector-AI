"""
Resume SQLAlchemy model.
"""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.engine import Base

if TYPE_CHECKING:
    from app.models.application import Application
    from app.models.skill import ResumeSkill
    from app.models.user import User


class Resume(Base):
    """
    Candidate Resume document model.
    """

    __tablename__ = "resumes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    file_path: Mapped[str] = mapped_column(String(512), nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    
    raw_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    parsed_data: Mapped[Dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    
    # Store sentence-transformer vector embedding as PostgreSQL Float Array
    embedding: Mapped[List[float] | None] = mapped_column(ARRAY(Float), nullable=True)
    ats_score: Mapped[float | None] = mapped_column(Float, nullable=True)

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
    user: Mapped["User"] = relationship("User", backref="resumes")
    resume_skills: Mapped[List["ResumeSkill"]] = relationship("ResumeSkill", back_populates="resume", cascade="all, delete-orphan")
    applications: Mapped[List["Application"]] = relationship("Application", back_populates="resume", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Resume id={self.id} user_id={self.user_id} file_name={self.file_name!r}>"
