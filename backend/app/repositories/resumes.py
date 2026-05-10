"""Resume repository for database operations."""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import models
from app.repositories.base import BaseRepository


class ResumeRepository(BaseRepository):
    """Repository for resume operations."""

    def __init__(self, db: Session):
        super().__init__(db, models.Resume)

    def get_by_user(self, user_id: uuid.UUID, limit: int = 100, offset: int = 0) -> list[models.Resume]:
        """Get all resumes for a user."""
        return self.db.execute(
            select(models.Resume)
            .where(models.Resume.user_id == user_id)
            .order_by(models.Resume.uploaded_at.desc())
            .limit(limit)
            .offset(offset)
        ).scalars().all()

    def get_by_user_and_filename(self, user_id: uuid.UUID, filename: str) -> models.Resume | None:
        """Get a resume by user and filename."""
        return self.db.execute(
            select(models.Resume).where(
                models.Resume.user_id == user_id,
                models.Resume.filename == filename,
            )
        ).scalar_one_or_none()

    def get_filenames_by_user(self, user_id: uuid.UUID) -> list[str]:
        """Get all filenames for a user (for duplicate detection)."""
        return self.db.execute(
            select(models.Resume.filename).where(
                models.Resume.user_id == user_id,
            )
        ).scalars().all()

    def count_by_user(self, user_id: uuid.UUID) -> int:
        """Count resumes for a user."""
        return self.db.execute(
            select(models.func.count())
            .select_from(models.Resume)
            .where(models.Resume.user_id == user_id)
        ).scalar()

    def get_by_user_and_id(self, user_id: uuid.UUID, resume_id: uuid.UUID) -> models.Resume | None:
        """Get a specific resume ensuring user ownership."""
        return self.db.execute(
            select(models.Resume).where(
                models.Resume.id == resume_id,
                models.Resume.user_id == user_id,
            )
        ).scalar_one_or_none()

    def delete_by_user_and_id(self, user_id: uuid.UUID, resume_id: uuid.UUID) -> bool:
        """Delete a resume ensuring user ownership. Returns True if deleted."""
        resume = self.get_by_user_and_id(user_id, resume_id)
        if resume:
            self.delete(resume)
            return True
        return False