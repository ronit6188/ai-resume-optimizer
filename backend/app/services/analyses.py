"""Analysis service with business logic."""

from __future__ import annotations

import logging
import uuid

from sqlalchemy.orm import Session

from app.db import models
from app.repositories.analyses import AnalysisRepository
from app.repositories.resumes import ResumeRepository
from app.repositories.jobs import JobRepository
from app.ai.analyzer import AIAnalysisEngine
from app.exceptions import NotFoundError, AIAnalysisError

logger = logging.getLogger(__name__)


class AnalysisService:
    """Service for analysis operations."""

    def __init__(self, db: Session):
        self.db = db
        self.repo = AnalysisRepository(db)
        self.resume_repo = ResumeRepository(db)
        self.job_repo = JobRepository(db)
        self.ai_service = AIAnalysisEngine()

    def create(
        self,
        user_id: uuid.UUID,
        resume_id: uuid.UUID,
        job_desc_id: uuid.UUID | None,
    ) -> models.Analysis:
        """Create a new analysis."""
        logger.info("Step 1: Fetching resume")
        resume = self.resume_repo.get_by_user_and_id(user_id, resume_id)
        if not resume:
            raise NotFoundError("Resume", str(resume_id))
        logger.info("Step 1: Resume fetched", extra={"extracted_text_length": len(resume.extracted_text or "")})

        job_desc = None
        if job_desc_id:
            logger.info("Step 2: Fetching job description")
            job_desc = self.job_repo.get_by_user_and_id(user_id, job_desc_id)
            if not job_desc:
                raise NotFoundError("Job description", str(job_desc_id))

        logger.info(
            "Creating analysis",
            extra={
                "user_id": str(user_id),
                "resume_id": str(resume_id),
                "job_desc_id": str(job_desc_id) if job_desc_id else None,
            },
        )

        logger.info("Step 3: Running AI analysis")
        ai_result = self.ai_service.analyze(
            resume_text=resume.extracted_text or "",
            job_description_text=job_desc.description_text if job_desc else None,
        )
        logger.info("Step 3: AI analysis complete", extra={"keys": list(ai_result.keys())})

        if ai_result.get("_error"):
            logger.error("AI analysis failed", extra={"error": ai_result.get("_error")})
            raise AIAnalysisError("Failed to generate analysis")

        logger.info(
            "Analysis completed",
            extra={"user_id": str(user_id), "score": ai_result.get("overall_score")},
        )

        logger.info("Step 4: Creating DB record")
        try:
            result = self.repo.create(
                id=uuid.uuid4(),
                user_id=user_id,
                resume_id=resume_id,
                job_desc_id=job_desc_id,
                ats_score=ai_result.get("overall_score"),
                keyword_matches=ai_result.get("keyword_matches"),
                missing_keywords=ai_result.get("missing_keywords"),
                weak_sections=ai_result.get("weak_sections"),
                suggestions=ai_result.get("suggestions"),
                rewritten_bullets=ai_result.get("rewritten_bullets"),
                overall_score=ai_result.get("overall_score"),
                seniority_classification=ai_result.get("seniority_classification"),
                score_categories=ai_result.get("score_categories"),
                keyword_analysis=ai_result.get("keyword_analysis"),
                resume_structure=ai_result.get("resume_structure"),
                experience_quality=ai_result.get("experience_quality"),
                technical_analysis=ai_result.get("technical_analysis"),
                writing_quality=ai_result.get("writing_quality"),
                job_analysis=ai_result.get("job_analysis"),
                recruiter_simulation=ai_result.get("recruiter_simulation"),
                missing_skills=ai_result.get("missing_skills"),
                career_guidance=ai_result.get("career_guidance"),
                improved_bullets=ai_result.get("improved_bullets"),
                analysis_timestamp=ai_result.get("analysis_timestamp"),
            )
            logger.info("Step 4: DB record created", extra={"analysis_id": str(result.id)})
            return result
        except Exception as e:
            logger.error("Step 4: DB create failed", exc_info=True, extra={"error": str(e), "error_type": type(e).__name__})
            raise

    def list_by_user(self, user_id: uuid.UUID) -> list[models.Analysis]:
        """List all analyses for a user."""
        return self.repo.get_by_user(user_id)

    def get_for_user(self, user_id: uuid.UUID, analysis_id: uuid.UUID) -> models.Analysis:
        """Get a specific analysis for a user."""
        analysis = self.repo.get_by_user_and_id(user_id, analysis_id)
        if not analysis:
            raise NotFoundError("Analysis", str(analysis_id))
        return analysis

    def delete_by_resume(self, resume_id: uuid.UUID) -> int:
        """Delete all analyses for a resume."""
        return self.repo.delete_by_resume(resume_id)

    def count_for_user(self, user_id: uuid.UUID) -> int:
        """Count analyses for a user."""
        return self.repo.count_by_user(user_id)

    def delete_for_user(self, user_id: uuid.UUID, analysis_id: uuid.UUID) -> bool:
        """Delete an analysis for a user."""
        logger.info("Deleting analysis", extra={"user_id": str(user_id), "analysis_id": str(analysis_id)})
        return self.repo.delete_by_user_and_id(user_id, analysis_id)