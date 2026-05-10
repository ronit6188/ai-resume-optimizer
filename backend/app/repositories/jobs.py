"""Job description repository for database operations."""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import models
from app.repositories.base import BaseRepository


class JobRepository(BaseRepository):
    """Repository for job description operations."""

    def __init__(self, db: Session):
        super().__init__(db, models.JobDescription)

    def get_by_user(self, user_id: uuid.UUID, limit: int = 100, offset: int = 0) -> list[models.JobDescription]:
        """Get all job descriptions for a user."""
        return self.db.execute(
            select(models.JobDescription)
            .where(models.JobDescription.user_id == user_id)
            .order_by(models.JobDescription.uploaded_at.desc())
            .limit(limit)
            .offset(offset)
        ).scalars().all()

    def get_by_user_and_id(self, user_id: uuid.UUID, job_id: uuid.UUID) -> models.JobDescription | None:
        """Get a specific job description ensuring user ownership."""
        return self.db.execute(
            select(models.JobDescription).where(
                models.JobDescription.id == job_id,
                models.JobDescription.user_id == user_id,
            )
        ).scalar_one_or_none()

    def count_by_user(self, user_id: uuid.UUID) -> int:
        """Count job descriptions for a user."""
        return self.db.execute(
            select(models.func.count())
            .select_from(models.JobDescription)
            .where(models.JobDescription.user_id == user_id)
        ).scalar()