"""SQLAlchemy engine and session helper for PostgreSQL."""

from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool, QueuePool

from ..core.config import settings


def get_engine_options():
    """Get engine options based on database type."""
    if settings.DATABASE_URL.startswith("postgresql"):
        return {
            "poolclass": QueuePool,
            "pool_size": settings.DATABASE_POOL_SIZE,
            "max_overflow": settings.DATABASE_MAX_OVERFLOW,
            "pool_timeout": settings.DATABASE_POOL_TIMEOUT,
            "pool_pre_ping": True,
            "pool_recycle": 3600,
        }
    elif settings.DATABASE_URL.startswith("sqlite"):
        return {
            "poolclass": NullPool,
            "connect_args": {"check_same_thread": False},
        }
    return {}


engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.SQLALCHEMY_ECHO,
    future=True,
    **get_engine_options(),
)


@event.listens_for(engine, "connect")
def set_search_path(dbapi_connection, connection_record):
    """Set PostgreSQL search path on connection."""
    if settings.DATABASE_URL.startswith("postgresql"):
        cursor = dbapi_connection.cursor()
        cursor.execute("SET search_path TO public")
        cursor.close()


SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


def get_db() -> Generator[Session, None, None]:
    """Database session dependency for FastAPI routes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context() -> Generator[Session, None, None]:
    """Context manager for database sessions outside of FastAPI."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


get_async_session = get_db