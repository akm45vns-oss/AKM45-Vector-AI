"""
FastAPI dependency injection — authentication and authorisation.

Usage in routers:

    from app.core.dependencies import get_current_user, require_role

    @router.get("/me")
    async def get_me(current_user: User = Depends(get_current_user)):
        ...

    @router.post("/jobs")
    async def create_job(
        current_user: User = Depends(require_role(UserRole.RECRUITER, UserRole.ADMIN))
    ):
        ...
"""

import uuid
from typing import Annotated

import structlog
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token
from app.database.engine import get_db
from app.models.user import User, UserRole

logger = structlog.get_logger(__name__)

# Bearer token extractor — reads "Authorization: Bearer <token>"
bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None, Depends(bearer_scheme)
    ],
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Extract and validate the JWT from the Authorization header.
    Returns the authenticated User ORM object.

    Raises HTTP 401 if the token is missing, invalid, or expired.
    Raises HTTP 403 if the user is inactive or unverified.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None:
        raise credentials_exception

    try:
        payload = decode_token(credentials.credentials)
    except JWTError:
        raise credentials_exception

    if payload.type != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type — expected access token",
        )

    try:
        user_id = uuid.UUID(payload.sub)
    except (ValueError, AttributeError):
        raise credentials_exception

    # Inline import to avoid circular deps
    from app.repositories.user_repository import UserRepository
    repo = UserRepository(db)
    user = await repo.get_by_id(user_id)

    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated. Contact support.",
        )

    return user


async def get_current_verified_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Like get_current_user but also requires email verification.
    Use this on sensitive endpoints.
    """
    if not current_user.is_email_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email address not verified. Please check your inbox.",
        )
    return current_user


def require_role(*roles: UserRole):
    """
    Role-based access control dependency factory.

    Example::

        Depends(require_role(UserRole.RECRUITER, UserRole.ADMIN))
    """

    async def _check_role(
        current_user: User = Depends(get_current_verified_user),
    ) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required role(s): {[r.value for r in roles]}",
            )
        return current_user

    return _check_role


# ── Typed aliases for convenience ─────────────────────────────────────────────
CurrentUser = Annotated[User, Depends(get_current_user)]
CurrentVerifiedUser = Annotated[User, Depends(get_current_verified_user)]
AdminUser = Annotated[User, Depends(require_role(UserRole.ADMIN))]
RecruiterUser = Annotated[User, Depends(require_role(UserRole.RECRUITER, UserRole.ADMIN))]
CandidateUser = Annotated[User, Depends(require_role(UserRole.CANDIDATE))]

# ── DB session alias ──────────────────────────────────────────────────────────
DBSession = Annotated[AsyncSession, Depends(get_db)]
