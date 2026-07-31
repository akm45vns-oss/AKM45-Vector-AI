"""
Database engine and session management using SQLAlchemy async.
"""

from typing import AsyncGenerator

import structlog
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool

from app.core.config import settings

logger = structlog.get_logger(__name__)


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""
    pass


def _build_engine() -> AsyncEngine:
    """Create an async SQLAlchemy engine with appropriate pool settings."""
    kwargs: dict = {
        "echo": settings.DEBUG,
        "future": True,
    }

    # Neon (serverless) requires NullPool — no persistent connections
    if "neon.tech" in settings.DATABASE_URL:
        kwargs["poolclass"] = NullPool
        logger.info("Using NullPool for Neon serverless database")
    else:
        kwargs.update(
            {
                "pool_size": 10,
                "max_overflow": 20,
                "pool_pre_ping": True,
                "pool_recycle": 300,
            }
        )

    return create_async_engine(settings.DATABASE_URL, **kwargs)


engine: AsyncEngine = _build_engine()

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that yields a database session.

    Usage::

        @router.get("/items")
        async def list_items(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def create_db_tables() -> None:
    """
    Create all database tables.
    Used in development — production uses Alembic migrations.
    """
    # Import all models so Base.metadata is populated
    from app.models import user, company, job, resume, application, skill  # noqa: F401

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created/verified")
