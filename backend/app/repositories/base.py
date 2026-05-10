"""Base repository with common database operations."""

from __future__ import annotations

import uuid
from typing import Any, TypeVar

from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.exceptions import DatabaseError, DuplicateError, NotFoundError

ModelType = TypeVar("ModelType")


class BaseRepository:
    """Base repository with common CRUD operations."""

    def __init__(self, db: Session, model: type[ModelType]):
        self.db = db
        self.model = model

    def _handle_db_error(self, operation: str, error: Exception) -> None:
        """Handle database errors consistently."""
        if isinstance(error, IntegrityError):
            raise DatabaseError(
                f"Integrity error during {operation}: resource may already exist",
                details={"operation": operation},
            )
        if isinstance(error, SQLAlchemyError):
            raise DatabaseError(
                f"Database error during {operation}",
                details={"operation": operation, "error": str(error)},
            )
        raise error

    def get_by_id(self, id: uuid.UUID) -> ModelType | None:
        """Get a single record by ID."""
        return self.db.execute(
            select(self.model).where(self.model.id == id)
        ).scalar_one_or_none()

    def get_by_id_or_raise(self, id: uuid.UUID, resource_name: str = "Resource") -> ModelType:
        """Get a record by ID or raise NotFoundError."""
        result = self.get_by_id(id)
        if not result:
            raise NotFoundError(resource_name, str(id))
        return result

    def get_all(self, limit: int = 100, offset: int = 0) -> list[ModelType]:
        """Get all records with pagination."""
        return self.db.execute(
            select(self.model).limit(limit).offset(offset)
        ).scalars().all()

    def count(self) -> int:
        """Count total records."""
        return self.db.execute(select(func.count()).select_from(self.model)).scalar()

    def create(self, **kwargs) -> ModelType:
        """Create a new record."""
        try:
            instance = self.model(**kwargs)
            self.db.add(instance)
            self.db.commit()
            self.db.refresh(instance)
            return instance
        except IntegrityError as e:
            self.db.rollback()
            raise DuplicateError(self.model.__name__, "unique field")
        except SQLAlchemyError as e:
            self.db.rollback()
            self._handle_db_error("create", e)

    def update(self, instance: ModelType, **kwargs) -> ModelType:
        """Update an existing record."""
        try:
            for key, value in kwargs.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)
            self.db.commit()
            self.db.refresh(instance)
            return instance
        except SQLAlchemyError as e:
            self.db.rollback()
            self._handle_db_error("update", e)

    def delete(self, instance: ModelType) -> None:
        """Delete a record."""
        try:
            self.db.delete(instance)
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            self._handle_db_error("delete", e)

    def exists(self, **filters) -> bool:
        """Check if a record exists with given filters."""
        result = self.db.execute(
            select(self.model).filter_by(**filters).limit(1)
        ).scalar_one_or_none()
        return result is not None