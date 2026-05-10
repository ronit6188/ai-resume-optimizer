"""Error tracking and monitoring configuration.

This module provides:
- Sentry integration for error tracking
- Severity levels and triage workflows
- Structured logging with context
- Health monitoring endpoints
"""

from __future__ import annotations

import logging
import os
import sys
from enum import Enum
from typing import Any

import structlog
from pydantic import BaseModel
from starlette.responses import JSONResponse
from sentry_sdk import Hub, add_breadcrumb, init
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

from .config import settings
from .logger import logger


class ErrorSeverity(str, Enum):
    """Severity levels for error classification."""

    CRITICAL = "critical"  # System down, data loss, security breach
    HIGH = "high"  # Major feature broken, significant degradation
    MEDIUM = "medium"  # Feature degraded, workarounds available
    LOW = "low"  # Minor issue, cosmetic, low impact
    INFO = "info"  # Informational, not an error


class ErrorCategory(str, Enum):
    """Categories for error classification."""

    DATABASE = "database"
    AUTHENTICATION = "authentication"
    VALIDATION = "validation"
    EXTERNAL_API = "external_api"
    FILE_PROCESSING = "file_processing"
    SECURITY = "security"
    RATE_LIMIT = "rate_limit"
    UNKNOWN = "unknown"


def get_severity_from_status_code(status_code: int) -> ErrorSeverity:
    """Map HTTP status codes to severity levels."""
    if status_code >= 500:
        return ErrorSeverity.CRITICAL
    elif status_code >= 400:
        return ErrorSeverity.MEDIUM
    return ErrorSeverity.LOW


def capture_error(
    error: Exception,
    category: ErrorCategory = ErrorCategory.UNKNOWN,
    severity: ErrorSeverity = ErrorSeverity.MEDIUM,
    context: dict[str, Any] | None = None,
) -> None:
    """
    Capture and track an error with structured context.
    
    Args:
        error: The exception to track
        category: Category of the error for triage
        severity: Severity level
        context: Additional context for debugging
    """
    extra_context = {
        "error_category": category.value,
        "error_severity": severity.value,
        "error_type": type(error).__name__,
    }
    if context:
        extra_context.update(context)
    
    logger.error(
        "error_captured",
        error=str(error),
        **extra_context
    )
    
    # Capture in Sentry if available
    current_scope = Hub.current.scope
    current_scope.set_tag("category", category.value)
    current_scope.set_tag("severity", severity.value)
    
    if severity in [ErrorSeverity.CRITICAL, ErrorSeverity.HIGH]:
        capture_message(
            f"{category.value}: {str(error)}",
            level="error" if severity == ErrorSeverity.HIGH else "fatal"
        )


def capture_message(
    message: str,
    level: str = "info",
    context: dict[str, Any] | None = None,
) -> None:
    """Capture a message with optional context."""
    from sentry_sdk import capture_message as sentry_capture_message

    sentry_capture_message(message, level=level, extras=context or {})


def add_breadcrumb(
    category: str,
    message: str,
    level: str = "info",
    data: dict[str, Any] | None = None,
) -> None:
    """Add a breadcrumb for tracing user actions."""
    add_breadcrumb(
        category=category,
        message=message,
        level=level,
        data=data or {},
    )


def setup_sentry(app: FastAPI) -> None:
    """
    Initialize Sentry for error tracking.
    
    Configure with:
    - DSN from environment or skip if not set
    - FastAPI integration for error tracking
    - SQLAlchemy integration for database errors
    - Performance monitoring
    - Environment-based configuration
    """
    sentry_dsn = os.environ.get("SENTRY_DSN")
    
    if not sentry_dsn:
        logger.warning("sentry_not_configured", message="Sentry DSN not set, skipping initialization")
        return
    
    # Don't capture in local dev unless explicitly enabled
    if settings.ENV == "dev" and not os.environ.get("SENTRY_ENABLE_DEV"):
        return
    
    integrations = [
        FastApiIntegration(app),
        StarletteIntegration(),
        SqlalchemyIntegration(),
    ]
    
    init(
        dsn=sentry_dsn,
        integrations=integrations,
        environment=settings.ENV,
        release=f"ai-resume-optimizer@{getattr(settings, 'VERSION', '0.1.0')}",
        traces_sample_rate=0.1 if settings.ENV == "prod" else 1.0,
        profiles_sample_rate=0.1 if settings.ENV == "prod" else 1.0,
        send_default_pii=False,  # Don't send PII to Sentry
        before_send=lambda event, hint: filter_sentry_event(event, hint),
    )
    
    logger.info("sentry_initialized", environment=settings.ENV, dsn_prefix=sentry_dsn[:20] + "...")


def filter_sentry_event(event: dict, hint: dict) -> dict | None:
    """
    Filter events before sending to Sentry.
    
    Remove noise from common non-critical errors.
    """
    # Filter out rate limiting 429s in production
    if settings.ENV == "prod":
        exc_info = hint.get("exc_info")
        if exc_info and hasattr(exc_info[1], "status_code"):
            if exc_info[1].status_code == 429:
                return None
    
    return event


class HealthResponse(BaseModel):
    """Health check response model."""
    
    status: str
    version: str
    timestamp: str
    checks: dict[str, str]


def create_health_endpoint(app: FastAPI) -> None:
    """Add health check and monitoring endpoints."""
    
    @app.get("/health", response_model=HealthResponse, tags=["monitoring"])
    async def health_check() -> HealthResponse:
        """Basic health check endpoint."""
        from datetime import datetime
        
        return HealthResponse(
            status="healthy",
            version="0.1.0",
            timestamp=datetime.utcnow().isoformat(),
            checks={"database": "ok", "api": "ok"}
        )
    
    @app.get("/health/ready", tags=["monitoring"])
    async def readiness_check() -> JSONResponse:
        """
        Readiness probe - checks if the service can handle requests.
        
        Returns 503 if not ready.
        """
        from datetime import datetime
        
        checks = {}
        is_ready = True
        
        # Check database connection
        try:
            from app.db.session import engine
            with engine.connect() as conn:
                conn.execute("SELECT 1")
            checks["database"] = "ok"
        except Exception as e:
            checks["database"] = f"error: {str(e)}"
            is_ready = False
        
        if is_ready:
            return JSONResponse(
                status_code=200,
                content={
                    "status": "ready",
                    "timestamp": datetime.utcnow().isoformat(),
                    "checks": checks
                }
            )
        else:
            return JSONResponse(
                status_code=503,
                content={
                    "status": "not_ready",
                    "timestamp": datetime.utcnow().isoformat(),
                    "checks": checks
                }
            )
    
    @app.get("/health/live", tags=["monitoring"])
    async def liveness_check() -> JSONResponse:
        """
        Liveness probe - checks if the service is running.
        
        Simple check that doesn't verify dependencies.
        """
        from datetime import datetime
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "alive",
                "timestamp": datetime.utcnow().isoformat()
            }
        )


def create_error_handlers(app: FastAPI) -> None:
    """
    Create global exception handlers for the FastAPI app.
    
    Handles:
    - Generic exceptions
    - HTTP exceptions
    - Validation errors
    - Database errors
    """
    from fastapi.exceptions import RequestValidationError
    from starlette.exceptions import HTTPException as StarletteHTTPException
    from sqlalchemy.exc import SQLAlchemyError
    
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        severity = get_severity_from_status_code(exc.status_code)
        
        logger.warning(
            "http_error",
            status_code=exc.status_code,
            detail=exc.detail,
            path=request.url.path,
            severity=severity.value
        )
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.detail,
                "status_code": exc.status_code,
                "path": str(request.url.path),
            }
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        errors = exc.errors()
        
        logger.warning(
            "validation_error",
            errors=errors,
            path=request.url.path,
            severity=ErrorSeverity.MEDIUM.value
        )
        
        return JSONResponse(
            status_code=422,
            content={
                "error": "Validation failed",
                "details": errors,
                "path": str(request.url.path),
            }
        )
    
    @app.exception_handler(SQLAlchemyError)
    async def database_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
        capture_error(
            exc,
            category=ErrorCategory.DATABASE,
            severity=ErrorSeverity.HIGH,
            context={"path": str(request.url.path)}
        )
        
        logger.error(
            "database_error",
            error=str(exc),
            path=request.url.path
        )
        
        return JSONResponse(
            status_code=500,
            content={
                "error": "Database error occurred",
                "status_code": 500,
            }
        )
    
    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        capture_error(
            exc,
            category=ErrorCategory.UNKNOWN,
            severity=ErrorSeverity.HIGH,
            context={
                "path": str(request.url.path),
                "method": request.method,
            }
        )
        
        logger.error(
            "unhandled_exception",
            error=str(exc),
            error_type=type(exc).__name__,
            path=request.url.path
        )
        
        return JSONResponse(
            status_code=500,
            content={
                "error": "An unexpected error occurred",
                "status_code": 500,
            }
        )