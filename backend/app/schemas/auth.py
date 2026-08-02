"""
Pydantic schemas for authentication endpoints.
Request bodies, response models, and internal transfer objects.
"""

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.models.user import UserRole


# ── Request Schemas ───────────────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    """Body for POST /auth/register"""
    name: str = Field(..., min_length=2, max_length=120, examples=["Jane Smith"])
    email: EmailStr = Field(..., examples=["jane@example.com"])
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        examples=["SecurePass123!"],
    )
    role: UserRole = Field(default=UserRole.CANDIDATE)

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Name cannot be blank")
        return v.strip()

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class LoginRequest(BaseModel):
    """Body for POST /auth/login"""
    email: EmailStr = Field(..., examples=["jane@example.com"])
    password: str = Field(..., min_length=1, examples=["SecurePass123!"])


class RefreshTokenRequest(BaseModel):
    """Body for POST /auth/refresh"""
    refresh_token: str = Field(..., min_length=1)


class ForgotPasswordRequest(BaseModel):
    """Body for POST /auth/forgot-password"""
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """Body for POST /auth/reset-password"""
    token: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8, max_length=128)

    @field_validator("new_password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v


class VerifyEmailRequest(BaseModel):
    """Body for POST /auth/verify-email"""
    token: str = Field(..., min_length=1)


class UpdateProfileRequest(BaseModel):
    """Body for PATCH /auth/me"""
    name: Optional[str] = Field(None, min_length=2, max_length=120)
    bio: Optional[str] = Field(None, max_length=1000)
    avatar_url: Optional[str] = Field(None, max_length=512)


UserUpdateRequest = UpdateProfileRequest


# ── Response Schemas ──────────────────────────────────────────────────────────

class UserResponse(BaseModel):
    """Public user representation — never expose password_hash."""
    id: uuid.UUID
    name: str
    email: EmailStr
    role: UserRole
    is_active: bool
    is_email_verified: bool
    avatar_url: Optional[str]
    bio: Optional[str]
    created_at: datetime
    last_login_at: Optional[datetime]

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    """Returned on successful login or token refresh."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds until access token expiry
    user: UserResponse


class AccessTokenResponse(BaseModel):
    """Returned on token refresh (new access token only)."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class MessageResponse(BaseModel):
    """Generic success message response."""
    message: str
    success: bool = True


# ── Internal Transfer Objects ─────────────────────────────────────────────────

class TokenPayload(BaseModel):
    """JWT payload decoded by security module."""
    sub: str          # user UUID as string
    role: str         # UserRole value
    type: str         # "access" or "refresh"
    exp: Optional[int] = None
    iat: Optional[int] = None
