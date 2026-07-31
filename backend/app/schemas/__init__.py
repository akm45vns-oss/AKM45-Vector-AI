"""
Schemas package. Exports all Pydantic request/response schemas.
"""

from app.schemas.application import (
    ApplicationCreate,
    ApplicationResponse,
    ApplicationStatusUpdate,
)
from app.schemas.auth import (
    ForgotPasswordRequest,
    LoginRequest,
    RegisterRequest,
    ResetPasswordRequest,
    TokenResponse,
    UserResponse,
    UserUpdateRequest,
)
from app.schemas.company import (
    CompanyCreate,
    CompanyResponse,
    CompanyUpdate,
)
from app.schemas.job import (
    JobCreate,
    JobListFilter,
    JobResponse,
    JobUpdate,
    SkillRequirement,
)

__all__ = [
    "RegisterRequest",
    "LoginRequest",
    "TokenResponse",
    "UserResponse",
    "UserUpdateRequest",
    "ForgotPasswordRequest",
    "ResetPasswordRequest",
    "CompanyCreate",
    "CompanyUpdate",
    "CompanyResponse",
    "JobCreate",
    "JobUpdate",
    "JobResponse",
    "JobListFilter",
    "SkillRequirement",
    "ApplicationCreate",
    "ApplicationStatusUpdate",
    "ApplicationResponse",
]
