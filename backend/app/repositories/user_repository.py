"""
User repository — all database operations for the User model.
Follows the Repository Pattern: no business logic, only data access.
"""

import uuid
from typing import Optional, Sequence

import structlog
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User, UserRole

logger = structlog.get_logger(__name__)


class UserRepository:
    """Data access layer for the User model."""

    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    # ── Read ─────────────────────────────────────────────────────────────────

    async def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """Fetch a user by UUID. Returns None if not found."""
        result = await self._db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        """Fetch a user by email (case-insensitive). Returns None if not found."""
        result = await self._db.execute(
            select(User).where(User.email == email.lower().strip())
        )
        return result.scalar_one_or_none()

    async def get_by_verification_token(self, token: str) -> Optional[User]:
        """Fetch a user by their email verification token."""
        result = await self._db.execute(
            select(User).where(User.email_verification_token == token)
        )
        return result.scalar_one_or_none()

    async def get_by_reset_token(self, token: str) -> Optional[User]:
        """Fetch a user by their password reset token."""
        result = await self._db.execute(
            select(User).where(User.password_reset_token == token)
        )
        return result.scalar_one_or_none()

    async def list_by_role(
        self, role: UserRole, *, limit: int = 50, offset: int = 0
    ) -> Sequence[User]:
        """List users by role with pagination."""
        result = await self._db.execute(
            select(User)
            .where(User.role == role, User.is_active.is_(True))
            .order_by(User.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()

    async def email_exists(self, email: str) -> bool:
        """Return True if the email is already registered."""
        result = await self._db.execute(
            select(User.id).where(User.email == email.lower().strip())
        )
        return result.scalar_one_or_none() is not None

    # ── Write ────────────────────────────────────────────────────────────────

    async def create(
        self,
        *,
        name: str,
        email: str,
        password_hash: str,
        role: UserRole,
        is_email_verified: bool = False,
        email_verification_token: Optional[str] = None,
    ) -> User:
        """Insert a new user and return the persisted instance."""
        user = User(
            name=name.strip(),
            email=email.lower().strip(),
            password_hash=password_hash,
            role=role,
            is_email_verified=is_email_verified,
            email_verification_token=email_verification_token,
        )
        self._db.add(user)
        await self._db.flush()  # get generated id without committing
        await self._db.refresh(user)
        logger.info("User created", user_id=str(user.id), role=role.value)
        return user

    async def update_last_login(self, user_id: uuid.UUID) -> None:
        """Stamp the last_login_at timestamp."""
        from datetime import datetime, timezone
        await self._db.execute(
            update(User)
            .where(User.id == user_id)
            .values(last_login_at=datetime.now(timezone.utc))
        )

    async def verify_email(self, user_id: uuid.UUID) -> None:
        """Mark the user's email as verified and clear the token."""
        await self._db.execute(
            update(User)
            .where(User.id == user_id)
            .values(is_email_verified=True, email_verification_token=None)
        )

    async def set_password_reset_token(
        self,
        user_id: uuid.UUID,
        token: str,
        expires_at,
    ) -> None:
        """Store a hashed password reset token with expiry."""
        await self._db.execute(
            update(User)
            .where(User.id == user_id)
            .values(
                password_reset_token=token,
                password_reset_expires=expires_at,
            )
        )

    async def update_password(
        self, user_id: uuid.UUID, new_password_hash: str
    ) -> None:
        """Update the password hash and clear the reset token."""
        await self._db.execute(
            update(User)
            .where(User.id == user_id)
            .values(
                password_hash=new_password_hash,
                password_reset_token=None,
                password_reset_expires=None,
            )
        )

    async def update_profile(
        self,
        user_id: uuid.UUID,
        *,
        name: Optional[str] = None,
        bio: Optional[str] = None,
        avatar_url: Optional[str] = None,
    ) -> Optional[User]:
        """Update mutable profile fields. Returns updated user."""
        values: dict = {}
        if name is not None:
            values["name"] = name.strip()
        if bio is not None:
            values["bio"] = bio
        if avatar_url is not None:
            values["avatar_url"] = avatar_url

        if not values:
            return await self.get_by_id(user_id)

        await self._db.execute(
            update(User).where(User.id == user_id).values(**values)
        )
        return await self.get_by_id(user_id)

    async def deactivate(self, user_id: uuid.UUID) -> None:
        """Soft-delete a user account."""
        await self._db.execute(
            update(User).where(User.id == user_id).values(is_active=False)
        )
