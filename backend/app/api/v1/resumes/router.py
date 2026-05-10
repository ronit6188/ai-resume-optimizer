"""Resume routes - thin layer using services."""

from __future__ import annotations

import logging
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core import security
from app.db.session import get_db
from app.schemas.resumes import ResumeListResponse, ResumeResponse
from app.services.resumes import ResumeService
from app.exceptions import AppException, FileProcessingError

router = APIRouter(prefix="/resumes", tags=["resumes"])

logger = logging.getLogger(__name__)


def _handle_app_exception(e: AppException) -> HTTPException:
    """Convert app exception to HTTP exception."""
    return HTTPException(status_code=e.status_code, detail=e.message)


@router.post("/", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: UploadFile = File(...),
    user=Depends(security.get_current_user),
    db: Session = Depends(get_db),
) -> ResumeResponse:
    """Upload a new resume."""
    user_uuid = uuid.UUID(user["sub"])

    try:
        content = await file.read()
        service = ResumeService(db)
        resume = service.create(
            user_id=user_uuid,
            filename=file.filename,
            content=content,
        )
        return ResumeResponse.model_validate(resume)
    except AppException as e:
        raise _handle_app_exception(e)
    except Exception as e:
        logger.error("Resume upload failed", extra={"user_id": str(user_uuid), "error": str(e)}, exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to upload resume")


@router.get("/", response_model=ResumeListResponse)
def list_resumes(
    user=Depends(security.get_current_user),
    db: Session = Depends(get_db),
) -> ResumeListResponse:
    """List all resumes for the current user."""
    user_uuid = uuid.UUID(user["sub"])
    service = ResumeService(db)
    resumes = service.list_by_user(user_uuid)
    return ResumeListResponse(resumes=resumes)


@router.delete("/{resume_id}")
def delete_resume(
    resume_id: str,
    user=Depends(security.get_current_user),
    db: Session = Depends(get_db),
) -> dict[str, str]:
    """Delete a resume."""
    user_uuid = uuid.UUID(user["sub"])
    resume_uuid = uuid.UUID(resume_id)

    try:
        service = ResumeService(db)
        deleted = service.delete_for_user(user_uuid, resume_uuid)
        if not deleted:
            raise HTTPException(status_code=404, detail="Resume not found")
        return {"detail": "Resume deleted successfully"}
    except AppException as e:
        raise _handle_app_exception(e)
    except Exception as e:
        logger.error("Resume deletion failed", extra={"resume_id": resume_id, "error": str(e)})
        raise HTTPException(status_code=500, detail="Failed to delete resume")