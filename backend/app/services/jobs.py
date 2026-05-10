"""Job description service with business logic."""

from __future__ import annotations

import logging
import uuid

from sqlalchemy.orm import Session

from app.db import models
from app.repositories.jobs import JobRepository
from app.validators.resumes import JobValidator
from app.exceptions import NotFoundError

logger = logging.getLogger(__name__)


class JobService:
    """Service for job description operations."""

    def __init__(self, db: Session):
        self.db = db
        self.repo = JobRepository(db)

    def create(
        self,
        user_id: uuid.UUID,
        title: str,
        description: str,
    ) -> models.JobDescription:
        """Create a new job description."""
        validator = JobValidator()
        clean_title = validator.validate_title(title)
        clean_description = validator.validate_description(description)

        logger.info(
            "Creating job description",
            extra={"user_id": str(user_id), "title": clean_title},
        )

        return self.repo.create(
            id=uuid.uuid4(),
            user_id=user_id,
            title=clean_title,
            description_text=clean_description,
        )

    def list_by_user(self, user_id: uuid.UUID) -> list[models.JobDescription]:
        """List all job descriptions for a user."""
        return self.repo.get_by_user(user_id)

    def get_for_user(self, user_id: uuid.UUID, job_id: uuid.UUID) -> models.JobDescription:
        """Get a specific job description for a user."""
        job = self.repo.get_by_user_and_id(user_id, job_id)
        if not job:
            raise NotFoundError("Job description", str(job_id))
        return job

    def calculate_match(
        self,
        user_id: uuid.UUID,
        resume_id: uuid.UUID,
        job_id: uuid.UUID,
    ) -> dict:
        """Calculate match between resume and job."""
        import re

        resume = self.repo.db.execute(
            models.db.select(models.Resume).where(
                models.Resume.id == resume_id,
                models.Resume.user_id == user_id,
            )
        ).scalar_one_or_none()

        if not resume:
            raise NotFoundError("Resume", str(resume_id))

        job = self.get_for_user(user_id, job_id)

        resume_words = set(re.findall(r"[a-zA-Z][a-zA-Z0-9+#.-]{1,}", (resume.extracted_text or "").lower()))
        job_words = set(re.findall(r"[a-zA-Z][a-zA-Z0-9+#.-]{1,}", job.description_text.lower()))
        overlap = sorted(resume_words.intersection(job_words))
        match_percent = int(len(overlap) / max(1, len(job_words)) * 100) if job_words else 0

        logger.info(
            "Calculated job match",
            extra={
                "resume_id": str(resume_id),
                "job_id": str(job_id),
                "match_percent": match_percent,
            },
        )

        return {"match_percent": match_percent, "matched_keywords": overlap[:50]}

    def count_for_user(self, user_id: uuid.UUID) -> int:
        """Count job descriptions for a user."""
        return self.repo.count_by_user(user_id)