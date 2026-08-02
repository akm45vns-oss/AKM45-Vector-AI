"""
Security utilities: password hashing (bcrypt) and JWT encode/decode.
All cryptographic operations are centralised here.
"""

import secrets
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
import structlog
from jose import JWTError, jwt

from app.core.config import settings
from app.schemas.auth import TokenPayload

logger = structlog.get_logger(__name__)

# ── Password hashing ─────────────────────────────────────────────────────────

def hash_password(plain_password: str) -> str:
    """Hash a plain-text password using bcrypt with 72-byte safe truncation."""
    pw_bytes = plain_password.encode("utf-8")[:72]
    salt = bcrypt.gensalt(rounds=settings.BCRYPT_ROUNDS)
    return bcrypt.hashpw(pw_bytes, salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain-text password against a bcrypt hash."""
    try:
        pw_bytes = plain_password.encode("utf-8")[:72]
        hash_bytes = hashed_password.encode("utf-8")
        return bcrypt.checkpw(pw_bytes, hash_bytes)
    except Exception:
        return False


# ── JWT tokens ───────────────────────────────────────────────────────────────

def _create_token(
    subject: str,
    role: str,
    token_type: str,
    expire_delta: timedelta,
) -> str:
    """
    Internal factory for creating signed JWT tokens.

    Args:
        subject: UUID of the user (as string)
        role: UserRole value
        token_type: "access" or "refresh"
        expire_delta: How long until the token expires
    """
    now = datetime.now(timezone.utc)
    expire = now + expire_delta

    payload = {
        "sub": subject,
        "role": role,
        "type": token_type,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
        "jti": str(uuid.uuid4()),  # unique token ID for revocation
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_access_token(user_id: str, role: str) -> str:
    """Create a short-lived JWT access token."""
    return _create_token(
        subject=user_id,
        role=role,
        token_type="access",
        expire_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )


def create_refresh_token(user_id: str, role: str) -> str:
    """Create a long-lived JWT refresh token."""
    return _create_token(
        subject=user_id,
        role=role,
        token_type="refresh",
        expire_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )


def decode_token(token: str) -> TokenPayload:
    """
    Decode and validate a JWT token.

    Raises:
        JWTError: If the token is invalid, expired, or malformed.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        return TokenPayload(**payload)
    except JWTError as exc:
        logger.warning("JWT decode failed", error=str(exc))
        raise


# ── Secure random tokens (email verification, password reset) ─────────────────

def generate_secure_token(length: int = 32) -> str:
    """Generate a cryptographically secure URL-safe token."""
    return secrets.token_urlsafe(length)


def generate_numeric_otp(digits: int = 6) -> str:
    """Generate a numeric OTP for email verification."""
    return str(secrets.randbelow(10 ** digits)).zfill(digits)
