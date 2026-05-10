"""Analysis routes - thin layer using services."""

from __future__ import annotations

import logging
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core import security
from app.db.session import get_db
from app.schemas.analyses import AnalysisCreatePayload, AnalysisListResponse, AnalysisResponse
from app.services.analyses import AnalysisService as ResumeAnalysisService
from app.ai.analyzer import AIResponseNormalizer
from app.exceptions import AppException
from app.db import models

router = APIRouter(prefix="/analyses", tags=["analyses"])

logger = logging.getLogger(__name__)

_normalizer = AIResponseNormalizer()


def _handle_app_exception(e: AppException) -> HTTPException:
    """Convert app exception to HTTP exception."""
    return HTTPException(status_code=e.status_code, detail=e.message)


def _normalize_analysis(analysis: models.Analysis) -> dict:
    """Normalize analysis for API response."""
    return {
        "id": str(analysis.id),
        "resume_id": str(analysis.resume_id),
        "job_desc_id": str(analysis.job_desc_id) if analysis.job_desc_id else None,
        "created_at": analysis.created_at,
        "ats_score": analysis.ats_score,
        "keyword_matches": _normalizer.normalize_keyword_matches(analysis.keyword_matches),
        "missing_keywords": _normalizer.normalize_list_field(analysis.missing_keywords),
        "weak_sections": _normalizer.normalize_weak_sections(analysis.weak_sections),
        "suggestions": _normalizer.normalize_list_field(analysis.suggestions),
        "rewritten_bullets": _normalizer.normalize_list_field(analysis.rewritten_bullets),
        "overall_score": analysis.overall_score,
        "seniority_classification": analysis.seniority_classification,
        "score_categories": _normalizer.normalize_score_categories(analysis.score_categories),
        "keyword_analysis": analysis.keyword_analysis,
        "resume_structure": analysis.resume_structure,
        "experience_quality": analysis.experience_quality,
        "technical_analysis": analysis.technical_analysis,
        "writing_quality": analysis.writing_quality,
        "job_analysis": analysis.job_analysis,
        "recruiter_simulation": analysis.recruiter_simulation,
        "missing_skills": analysis.missing_skills,
        "career_guidance": analysis.career_guidance,
        "improved_bullets": analysis.improved_bullets,
        "analysis_timestamp": analysis.analysis_timestamp,
    }


@router.post("/", response_model=AnalysisResponse, status_code=status.HTTP_201_CREATED)
def create_analysis(
    payload: AnalysisCreatePayload,
    user=Depends(security.get_current_user),
    db: Session = Depends(get_db),
) -> AnalysisResponse:
    """Create a new analysis."""
    user_uuid = uuid.UUID(user["sub"])

    try:
        service = ResumeAnalysisService(db)
        analysis = service.create(
            user_id=user_uuid,
            resume_id=uuid.UUID(payload.resume_id),
            job_desc_id=uuid.UUID(payload.job_desc_id) if payload.job_desc_id else None,
        )
        normalized = _normalize_analysis(analysis)
        return AnalysisResponse(**normalized)
    except AppException as e:
        raise _handle_app_exception(e)
    except Exception as e:
        logger.error("Analysis creation failed", extra={"user_id": str(user_uuid), "error": str(e)}, exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to create analysis: {type(e).__name__}: {str(e)}")


@router.get("/", response_model=AnalysisListResponse)
def list_analyses(
    user=Depends(security.get_current_user),
    db: Session = Depends(get_db),
) -> AnalysisListResponse:
    """List all analyses for the current user."""
    user_uuid = uuid.UUID(user["sub"])
    service = ResumeAnalysisService(db)
    analyses = service.list_by_user(user_uuid)
    normalized = [_normalize_analysis(a) for a in analyses]
    return AnalysisListResponse(analyses=[AnalysisResponse(**n) for n in normalized])


@router.get("/{analysis_id}", response_model=AnalysisResponse)
def get_analysis(
    analysis_id: str,
    user=Depends(security.get_current_user),
    db: Session = Depends(get_db),
) -> AnalysisResponse:
    """Get a specific analysis."""
    user_uuid = uuid.UUID(user["sub"])

    try:
        service = ResumeAnalysisService(db)
        analysis = service.get_for_user(user_uuid, uuid.UUID(analysis_id))
        normalized = _normalize_analysis(analysis)
        return AnalysisResponse(**normalized)
    except AppException as e:
        raise _handle_app_exception(e)
    except Exception as e:
        logger.error("Analysis retrieval failed", extra={"analysis_id": analysis_id, "error": str(e)})
        raise HTTPException(status_code=500, detail="Failed to retrieve analysis")


@router.delete("/{analysis_id}")
def delete_analysis(
    analysis_id: str,
    user=Depends(security.get_current_user),
    db: Session = Depends(get_db),
) -> dict[str, str]:
    """Delete an analysis."""
    user_uuid = uuid.UUID(user["sub"])

    try:
        service = ResumeAnalysisService(db)
        deleted = service.delete_for_user(user_uuid, uuid.UUID(analysis_id))
        if not deleted:
            raise HTTPException(status_code=404, detail="Analysis not found")
        return {"detail": "Analysis deleted successfully"}
    except AppException as e:
        raise _handle_app_exception(e)
    except Exception as e:
        logger.error("Analysis deletion failed", extra={"analysis_id": analysis_id, "error": str(e)})
        raise HTTPException(status_code=500, detail="Failed to delete analysis")