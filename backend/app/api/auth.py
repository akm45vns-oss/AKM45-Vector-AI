"""
Authentication API router.
Replaces the Phase 1 stub with full production implementation.

Endpoints:
  POST /auth/register           — Create new account
  POST /auth/login              — Login + get tokens
  POST /auth/refresh            — Refresh token pair
  POST /auth/verify-email       — Confirm email address
  POST /auth/resend-verification — Resend verification email
  POST /auth/forgot-password    — Request password reset
  POST /auth/reset-password     — Set new password
  GET  /auth/me                 — Get current user profile
  PATCH /auth/me                — Update profile
  DELETE /auth/me               — Deactivate account
"""

import structlog
from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import CurrentUser, DBSession
from app.database.engine import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.auth import (
    ForgotPasswordRequest,
    LoginRequest,
    MessageResponse,
    RefreshTokenRequest,
    RegisterRequest,
    ResetPasswordRequest,
    TokenResponse,
    UpdateProfileRequest,
    UserResponse,
    VerifyEmailRequest,
)
from app.services.auth_service import AuthService

logger = structlog.get_logger(__name__)
router = APIRouter()


# ── Registration ──────────────────────────────────────────────────────────────

@router.post(
    "/register",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new account",
)
async def register(
    payload: RegisterRequest,
    db: DBSession,
) -> MessageResponse:
    """
    Create a new user account.

    - Validates email uniqueness
    - Hashes password with bcrypt
    - Sends email verification link via Resend
    - Returns success message (not the user object — they must verify email first)
    """
    service = AuthService(db)
    await service.register(payload)
    return MessageResponse(
        message=(
            f"Account created successfully. "
            f"A verification email has been sent to {payload.email}."
        )
    )


# ── Login ─────────────────────────────────────────────────────────────────────

@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login and receive JWT tokens",
)
async def login(
    payload: LoginRequest,
    db: DBSession,
) -> TokenResponse:
    """
    Authenticate with email and password.

    Returns access_token (30 min), refresh_token (7 days), and user profile.
    """
    service = AuthService(db)
    return await service.login(payload)


# ── Token Refresh ─────────────────────────────────────────────────────────────

@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh JWT tokens",
)
async def refresh_tokens(
    payload: RefreshTokenRequest,
    db: DBSession,
) -> TokenResponse:
    """
    Exchange a valid refresh token for a new access + refresh token pair.
    The old refresh token is effectively invalidated (rotation strategy).
    """
    service = AuthService(db)
    return await service.refresh_tokens(payload.refresh_token)


# ── Email Verification ────────────────────────────────────────────────────────

@router.post(
    "/verify-email",
    response_model=MessageResponse,
    summary="Verify email address",
)
async def verify_email(
    payload: VerifyEmailRequest,
    db: DBSession,
) -> MessageResponse:
    """Confirm a user's email using the token from the verification email."""
    service = AuthService(db)
    await service.verify_email(payload.token)
    return MessageResponse(message="Email verified successfully. You can now log in.")


@router.post(
    "/resend-verification",
    response_model=MessageResponse,
    summary="Resend verification email",
)
async def resend_verification(
    payload: ForgotPasswordRequest,  # reuse — just needs email
    db: DBSession,
) -> MessageResponse:
    """Resend the email verification link. Always returns 200 (no enumeration)."""
    service = AuthService(db)
    await service.resend_verification(payload.email)
    return MessageResponse(
        message="If that email is registered and unverified, a new verification link has been sent."
    )


# ── Forgot / Reset Password ───────────────────────────────────────────────────

@router.post(
    "/forgot-password",
    response_model=MessageResponse,
    summary="Request password reset email",
)
async def forgot_password(
    payload: ForgotPasswordRequest,
    db: DBSession,
) -> MessageResponse:
    """
    Trigger a password reset email.
    Always returns 200 — never reveals whether an email is registered.
    """
    service = AuthService(db)
    await service.forgot_password(payload.email)
    return MessageResponse(
        message="If that email is registered, a password reset link has been sent."
    )


@router.post(
    "/reset-password",
    response_model=MessageResponse,
    summary="Set a new password using reset token",
)
async def reset_password(
    payload: ResetPasswordRequest,
    db: DBSession,
) -> MessageResponse:
    """Reset the user's password with a valid reset token (valid for 1 hour)."""
    service = AuthService(db)
    await service.reset_password(payload.token, payload.new_password)
    return MessageResponse(
        message="Password reset successfully. You can now log in with your new password."
    )


# ── Profile ───────────────────────────────────────────────────────────────────

@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
)
async def get_me(current_user: CurrentUser) -> UserResponse:
    """Return the authenticated user's profile."""
    return UserResponse.model_validate(current_user)


@router.patch(
    "/me",
    response_model=UserResponse,
    summary="Update profile",
)
async def update_me(
    payload: UpdateProfileRequest,
    current_user: CurrentUser,
    db: DBSession,
) -> UserResponse:
    """Update name, bio, or avatar_url for the authenticated user."""
    repo = UserRepository(db)
    updated = await repo.update_profile(
        current_user.id,
        name=payload.name,
        bio=payload.bio,
        avatar_url=payload.avatar_url,
    )
    return UserResponse.model_validate(updated)


@router.delete(
    "/me",
    response_model=MessageResponse,
    summary="Deactivate account",
)
async def deactivate_me(
    current_user: CurrentUser,
    db: DBSession,
) -> MessageResponse:
    """Soft-delete the authenticated user's account."""
    repo = UserRepository(db)
    await repo.deactivate(current_user.id)
    return MessageResponse(message="Account deactivated successfully.")
