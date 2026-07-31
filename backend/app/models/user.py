"""
User SQLAlchemy model.
Uses UUID primary keys, BCrypt hashed passwords, and an enum-based role system.
"""

import uuid
from datetime import datetime, timezone
from enum import Enum as PyEnum

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.engine import Base


class UserRole(str, PyEnum):
    """Role-based access control roles."""
    ADMIN = "admin"
    RECRUITER = "recruiter"
    CANDIDATE = "candidate"


class User(Base):
    """
    User account model.

    Supports three roles (admin, recruiter, candidate).
    Email verification is required before a user can access protected endpoints.
    Soft-delete via is_active flag.
    """

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="userrole", create_constraint=True),
        nullable=False,
        default=UserRole.CANDIDATE,
        index=True,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_email_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    # Tokens stored as opaque strings (short-lived, hashed on storage)
    email_verification_token: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )
    password_reset_token: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )
    password_reset_expires: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    avatar_url: Mapped[str | None] = mapped_column(String(512), nullable=True)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
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
    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # ── Relationships (populated in later phases) ─────────────
    # resumes: Mapped[list["Resume"]] = relationship(...)
    # company: Mapped["Company"] = relationship(...)

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email!r} role={self.role}>"
