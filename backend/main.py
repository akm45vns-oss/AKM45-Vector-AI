"""
HireSmart AI — FastAPI Application Entry Point

This module bootstraps the FastAPI application, registers all routers,
configures middleware, and sets up lifespan events.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from app.core.config import settings
from app.core.logging import setup_logging
from app.database.engine import create_db_tables, engine

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager — runs on startup and shutdown."""
    # ── Startup ──────────────────────────────────────────────
    setup_logging()
    logger.info("Starting HireSmart AI", version=settings.APP_VERSION, env=settings.ENVIRONMENT)

    # Create database tables (Alembic handles migrations in production)
    if settings.ENVIRONMENT == "development":
        await create_db_tables()
        logger.info("Database tables verified")

    logger.info("HireSmart AI is ready to serve requests")
    yield

    # ── Shutdown ─────────────────────────────────────────────
    logger.info("Shutting down HireSmart AI")
    await engine.dispose()
    logger.info("Database connections closed")


def create_application() -> FastAPI:
    """Factory function to create and configure the FastAPI app."""

    # ── Rate Limiter ─────────────────────────────────────────
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=[f"{settings.RATE_LIMIT_PER_MINUTE}/minute"],
    )

    app = FastAPI(
        title=settings.APP_NAME,
        description="AI-powered Applicant Tracking System — production-ready SaaS platform",
        version=settings.APP_VERSION,
        docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
        redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
        openapi_url="/openapi.json" if settings.ENVIRONMENT != "production" else None,
        lifespan=lifespan,
    )

    # ── State ────────────────────────────────────────────────
    app.state.limiter = limiter

    # ── Middleware ───────────────────────────────────────────
    app.add_middleware(SlowAPIMiddleware)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["X-Total-Count", "X-Request-ID"],
    )

    if settings.ENVIRONMENT == "production":
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=settings.TRUSTED_HOSTS,
        )

    # ── Exception Handlers ───────────────────────────────────
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # ── Routers (imported lazily to avoid circular imports) ──
    from app.api.auth import router as auth_router
    from app.api.resumes import router as resumes_router
    from app.api.jobs import router as jobs_router
    from app.api.applications import router as applications_router
    from app.api.matching import router as matching_router
    from app.api.analytics import router as analytics_router
    from app.api.companies import router as companies_router

    app.include_router(auth_router,         prefix="/auth",         tags=["Authentication"])
    app.include_router(resumes_router,      prefix="/resume",       tags=["Resumes"])
    app.include_router(jobs_router,         prefix="/jobs",         tags=["Jobs"])
    app.include_router(applications_router, prefix="/applications", tags=["Applications"])
    app.include_router(matching_router,     prefix="/matching",     tags=["Matching"])
    app.include_router(analytics_router,    prefix="/analytics",    tags=["Analytics"])
    app.include_router(companies_router,    prefix="/companies",    tags=["Companies"])

    return app


app = create_application()


@app.get("/health", tags=["System"])
async def health_check() -> JSONResponse:
    """Health check endpoint for Docker and load balancer."""
    return JSONResponse(
        content={
            "status": "healthy",
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT,
        }
    )


@app.get("/", tags=["System"])
async def root() -> JSONResponse:
    """Root endpoint."""
    return JSONResponse(
        content={
            "message": f"Welcome to {settings.APP_NAME} API",
            "docs": "/docs",
            "health": "/health",
        }
    )
