"""Analysis repository for database operations."""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import models
from app.repositories.base import BaseRepository


class AnalysisRepository(BaseRepository):
    """Repository for analysis operations."""

    def __init__(self, db: Session):
        super().__init__(db, models.Analysis)

    def get_by_user(self, user_id: uuid.UUID, limit: int = 100, offset: int = 0) -> list[models.Analysis]:
        """Get all analyses for a user."""
        return self.db.execute(
            select(models.Analysis)
            .where(models.Analysis.user_id == user_id)
            .order_by(models.Analysis.created_at.desc())
            .limit(limit)
            .offset(offset)
        ).scalars().all()

    def get_by_user_and_id(self, user_id: uuid.UUID, analysis_id: uuid.UUID) -> models.Analysis | None:
        """Get a specific analysis ensuring user ownership."""
        return self.db.execute(
            select(models.Analysis).where(
                models.Analysis.id == analysis_id,
                models.Analysis.user_id == user_id,
            )
        ).scalar_one_or_none()

    def get_by_resume(self, resume_id: uuid.UUID, limit: int = 100) -> list[models.Analysis]:
        """Get analyses for a specific resume."""
        return self.db.execute(
            select(models.Analysis)
            .where(models.Analysis.resume_id == resume_id)
            .order_by(models.Analysis.created_at.desc())
            .limit(limit)
        ).scalars().all()

    def count_by_user(self, user_id: uuid.UUID) -> int:
        """Count analyses for a user."""
        return self.db.execute(
            select(models.func.count())
            .select_from(models.Analysis)
            .where(models.Analysis.user_id == user_id)
        ).scalar()

    def count_by_resume(self, resume_id: uuid.UUID) -> int:
        """Count analyses for a resume."""
        return self.db.execute(
            select(models.func.count())
            .select_from(models.Analysis)
            .where(models.Analysis.resume_id == resume_id)
        ).scalar()

    def delete_by_resume(self, resume_id: uuid.UUID) -> int:
        """Delete all analyses for a resume. Returns count of deleted."""
        analyses = self.get_by_resume(resume_id)
        count = len(analyses)
        for analysis in analyses:
            self.db.delete(analysis)
        self.db.commit()
        return count

    def delete_by_user_and_id(self, user_id: uuid.UUID, analysis_id: uuid.UUID) -> bool:
        """Delete an analysis ensuring user ownership. Returns True if deleted."""
        analysis = self.get_by_user_and_id(user_id, analysis_id)
        if analysis:
            self.delete(analysis)
            return True
        return False