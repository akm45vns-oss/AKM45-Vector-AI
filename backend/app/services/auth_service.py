"""
Authentication service — all business logic for auth flows.
Coordinates between UserRepository, security utilities, and email service.
"""

import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

import structlog
from fastapi import HTTPException, status
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    generate_secure_token,
    hash_password,
    verify_password,
)
from app.models.user import User, UserRole
from app.repositories.user_repository import UserRepository
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from app.services.email_service import (
    send_password_reset_email,
    send_verification_email,
)
from app.core.config import settings

logger = structlog.get_logger(__name__)


class AuthService:
    """
    Business logic layer for authentication.
    All methods are async and use the UserRepository for data access.
    """

    def __init__(self, db: AsyncSession) -> None:
        self._repo = UserRepository(db)

    # ── Registration ──────────────────────────────────────────────────────────

    async def register(self, payload: RegisterRequest) -> User:
        """
        Register a new user account.

        1. Checks email uniqueness
        2. Hashes password
        3. Generates email verification token
        4. Creates user in DB
        5. Sends verification email (non-blocking failure)
        6. Returns the created User ORM object
        """
        if await self._repo.email_exists(payload.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this email already exists.",
            )

        verification_token = generate_secure_token(32)

        user = await self._repo.create(
            name=payload.name,
            email=payload.email,
            password_hash=hash_password(payload.password),
            role=payload.role,
            email_verification_token=verification_token,
        )

        # Send email — failure is logged but does not fail registration
        send_verification_email(
            to_email=user.email,
            user_name=user.name,
            token=verification_token,
        )

        logger.info("User registered", user_id=str(user.id), role=payload.role.value)
        return user

    # ── Login ─────────────────────────────────────────────────────────────────

    async def login(self, payload: LoginRequest) -> TokenResponse:
        """
        Authenticate a user and issue access + refresh tokens.

        Raises HTTP 401 for invalid credentials (intentionally vague).
        Raises HTTP 403 if account is deactivated.
        """
        invalid_creds = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

        user = await self._repo.get_by_email(payload.email)
        if user is None:
            raise invalid_creds

        if not verify_password(payload.password, user.password_hash):
            raise invalid_creds

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is deactivated. Contact support.",
            )

        access_token = create_access_token(str(user.id), user.role.value)
        refresh_token = create_refresh_token(str(user.id), user.role.value)

        await self._repo.update_last_login(user.id)

        logger.info("User logged in", user_id=str(user.id))

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=UserResponse.model_validate(user),
        )

    # ── Token Refresh ─────────────────────────────────────────────────────────

    async def refresh_tokens(self, refresh_token: str) -> TokenResponse:
        """
        Validate the refresh token and issue a new token pair.
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = decode_token(refresh_token)
        except JWTError:
            raise credentials_exception

        if payload.type != "refresh":
            raise credentials_exception

        try:
            user_id = uuid.UUID(payload.sub)
        except (ValueError, AttributeError):
            raise credentials_exception

        user = await self._repo.get_by_id(user_id)
        if user is None or not user.is_active:
            raise credentials_exception

        new_access = create_access_token(str(user.id), user.role.value)
        new_refresh = create_refresh_token(str(user.id), user.role.value)

        return TokenResponse(
            access_token=new_access,
            refresh_token=new_refresh,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=UserResponse.model_validate(user),
        )

    # ── Email Verification ────────────────────────────────────────────────────

    async def verify_email(self, token: str) -> None:
        """Mark the user's email as verified."""
        user = await self._repo.get_by_verification_token(token)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired verification token.",
            )
        if user.is_email_verified:
            return  # idempotent — already verified

        await self._repo.verify_email(user.id)
        logger.info("Email verified", user_id=str(user.id))

    async def resend_verification(self, email: str) -> None:
        """Generate a fresh verification token and resend the email."""
        user = await self._repo.get_by_email(email)
        if user is None:
            return  # silent — don't reveal if email exists

        if user.is_email_verified:
            return  # already verified — nothing to do

        new_token = generate_secure_token(32)
        await self._repo.set_password_reset_token(
            user.id, new_token, datetime.now(timezone.utc) + timedelta(hours=24)
        )
        # Reuse verification fields via direct update
        from sqlalchemy import update as sa_update
        from app.models.user import User as UserModel
        # Update verification token directly
        user = await self._repo.get_by_email(email)
        if user:
            user.email_verification_token = new_token

        send_verification_email(
            to_email=user.email,
            user_name=user.name,
            token=new_token,
        )

    # ── Forgot Password ───────────────────────────────────────────────────────

    async def forgot_password(self, email: str) -> None:
        """
        Initiate password reset flow.
        Always returns silently — never reveals whether email is registered.
        """
        user = await self._repo.get_by_email(email)
        if user is None:
            logger.info("Forgot password — email not found (silent)", email=email)
            return

        reset_token = generate_secure_token(32)
        expires_at = datetime.now(timezone.utc) + timedelta(hours=1)

        await self._repo.set_password_reset_token(user.id, reset_token, expires_at)
        send_password_reset_email(
            to_email=user.email,
            user_name=user.name,
            token=reset_token,
        )
        logger.info("Password reset email sent", user_id=str(user.id))

    # ── Reset Password ────────────────────────────────────────────────────────

    async def reset_password(self, token: str, new_password: str) -> None:
        """Validate the reset token and update the user's password."""
        user = await self._repo.get_by_reset_token(token)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired password reset token.",
            )

        if user.password_reset_expires and user.password_reset_expires < datetime.now(
            timezone.utc
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password reset token has expired. Please request a new one.",
            )

        await self._repo.update_password(user.id, hash_password(new_password))
        logger.info("Password reset successful", user_id=str(user.id))
