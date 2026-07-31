"""
Pytest fixtures shared across all tests.
Sets up an async test database (SQLite in-memory) and test client.
"""

import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.database.engine import Base, get_db
from main import app

# ── In-memory SQLite for tests ────────────────────────────────────────────────
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},
)

TestSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest_asyncio.fixture(scope="session")
async def db_setup():
    """Create all tables once per test session."""
    # Import all models so metadata is populated
    from app.models import user, company, job, resume, application, skill  # noqa
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db(db_setup) -> AsyncGenerator[AsyncSession, None]:
    """Fresh DB session for each test — rolls back after each test."""
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def client(db) -> AsyncGenerator[AsyncClient, None]:
    """Async HTTP test client with DB override."""

    async def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


# ── Test data factories ────────────────────────────────────────────────────────

@pytest.fixture
def candidate_payload():
    return {
        "name": "Alice Candidate",
        "email": "alice@test.com",
        "password": "TestPass123!",
        "role": "candidate",
    }


@pytest.fixture
def recruiter_payload():
    return {
        "name": "Bob Recruiter",
        "email": "bob@test.com",
        "password": "TestPass123!",
        "role": "recruiter",
    }
