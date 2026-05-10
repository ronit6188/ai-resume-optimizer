"""FastAPI entry point for AI Resume Analyzer and ATS Optimizer."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

from app.api.v1.analyses.router import router as analyses_router
from app.api.v1.auth.router import router as auth_router
from app.api.v1.jobs.router import router as jobs_router
from app.api.v1.resumes.router import router as resumes_router
from app.core.config import settings
from app.core.logger import logger
from app.core.monitoring import (
    create_error_handlers,
    create_health_endpoint,
    setup_sentry,
)
from app.db.base import Base
from app.db.session import engine


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    limiter = Limiter(key_func=get_remote_address, default_limits=[f"{settings.RATE_LIMIT_MAX}/minute"])

    app = FastAPI(
        title="AI Resume Analyzer & ATS Optimizer",
        version="0.1.0",
        description="Backend API for resume upload, analysis, and ATS scoring.",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # CORS middleware
    cors_origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",") if origin.strip()]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Rate limiting
    app.state.limiter = limiter
    app.add_exception_handler(429, _rate_limit_exceeded_handler)

    # Setup error tracking and monitoring
    setup_sentry(app)
    create_error_handlers(app)
    create_health_endpoint(app)

    @app.on_event("startup")
    def startup_event() -> None:
        """Initialize on startup."""
        logger.info("application_starting", version="0.1.0", environment=settings.ENV)
        
        # Create tables for SQLite, skip for PostgreSQL (use migrations)
        if "sqlite" in settings.DATABASE_URL:
            Base.metadata.create_all(bind=engine)
            logger.info("sqlite_tables_created")

    @app.on_event("shutdown")
    def shutdown_event() -> None:
        """Cleanup on shutdown."""
        logger.info("application_shutting_down")

    # API routes
    api_prefix = "/api/v1"
    app.include_router(auth_router, prefix=api_prefix)
    app.include_router(resumes_router, prefix=api_prefix)
    app.include_router(analyses_router, prefix=api_prefix)
    app.include_router(jobs_router, prefix=api_prefix)

    logger.info("app_created", routers=["auth", "resumes", "analyses", "jobs"])
    return app


app = create_app()