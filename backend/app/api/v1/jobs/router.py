"""Job description routes - thin layer using services."""

from __future__ import annotations

import logging
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core import security
from app.db.session import get_db
from app.schemas.jobs import JobCreatePayload, JobListResponse, JobResponse
from app.services.jobs import JobService
from app.exceptions import AppException

router = APIRouter(prefix="/jobs", tags=["jobs"])

logger = logging.getLogger(__name__)


def _handle_app_exception(e: AppException) -> HTTPException:
    """Convert app exception to HTTP exception."""
    return HTTPException(status_code=e.status_code, detail=e.message)


@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
def create_job(
    payload: JobCreatePayload,
    user=Depends(security.get_current_user),
    db: Session = Depends(get_db),
) -> JobResponse:
    """Create a new job description."""
    user_uuid = uuid.UUID(user["sub"])

    try:
        service = JobService(db)
        job = service.create(
            user_id=user_uuid,
            title=payload.title,
            description=payload.description,
        )
        return JobResponse.model_validate(job)
    except AppException as e:
        raise _handle_app_exception(e)
    except Exception as e:
        logger.error("Job creation failed", extra={"user_id": str(user_uuid), "error": str(e)})
        raise HTTPException(status_code=500, detail="Failed to create job description")


@router.get("/", response_model=JobListResponse)
def list_jobs(
    user=Depends(security.get_current_user),
    db: Session = Depends(get_db),
) -> JobListResponse:
    """List all job descriptions for the current user."""
    user_uuid = uuid.UUID(user["sub"])
    service = JobService(db)
    jobs = service.list_by_user(user_uuid)
    return JobListResponse(jobs=jobs)


class MatchPayload:
    """Match payload model."""

    def __init__(self, job_id: str, resume_id: str):
        self.job_id = job_id
        self.resume_id = resume_id


@router.post("/match")
def match_job(
    payload: dict,
    user=Depends(security.get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    """Calculate match between resume and job."""
    user_uuid = uuid.UUID(user["sub"])
    resume_id = payload.get("resume_id")
    job_id = payload.get("job_id")

    if not resume_id or not job_id:
        raise HTTPException(status_code=400, detail="resume_id and job_id are required")

    try:
        service = JobService(db)
        return service.calculate_match(user_uuid, uuid.UUID(resume_id), uuid.UUID(job_id))
    except AppException as e:
        raise _handle_app_exception(e)
    except Exception as e:
        logger.error("Job match failed", extra={"error": str(e)})
        raise HTTPException(status_code=500, detail="Failed to calculate match")