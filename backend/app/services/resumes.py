"""Resume service with business logic."""

from __future__ import annotations

import logging
import uuid

from sqlalchemy.orm import Session

from app.db import models
from app.repositories.resumes import ResumeRepository
from app.validators.resumes import ResumeValidator
from app.exceptions import NotFoundError, FileProcessingError
from app.utils import pdf_parser, validation

logger = logging.getLogger(__name__)


def generate_unique_filename(db: Session, user_id: uuid.UUID, original_filename: str) -> str:
    """Generate unique filename to avoid collisions."""
    repo = ResumeRepository(db)
    existing = set(repo.get_filenames_by_user(user_id))

    validator = ResumeValidator()
    filename = validator.validate_filename(original_filename)

    if filename not in existing:
        return filename

    base, ext = filename.rsplit(".", 1) if "." in filename else (filename, "")
    counter = 1
    while True:
        new_filename = f"{base}({counter}).{ext}" if ext else f"{base}({counter})"
        if new_filename not in existing:
            return new_filename
        counter += 1
        if counter > 1000:
            raise FileProcessingError("Unable to generate unique filename")


class ResumeService:
    """Service for resume operations."""

    def __init__(self, db: Session):
        self.db = db
        self.repo = ResumeRepository(db)

    def create(
        self,
        user_id: uuid.UUID,
        filename: str,
        content: bytes,
    ) -> models.Resume:
        """Create a new resume."""
        # Step 1: Validation
        logger.info("Step 1: Validating PDF content", extra={"size": len(content)})
        validation.validate_pdf_by_content(content)
        logger.info("Step 1: Validation passed")

        if len(content) > validation.MAX_PDF_SIZE:
            raise FileProcessingError("PDF size exceeds 5 MiB limit")

        # Step 2: Text extraction
        logger.info("Step 2: Extracting text from PDF")
        text = pdf_parser.extract_text_from_pdf(content)
        logger.info("Step 2: Extraction complete", extra={"text_length": len(text) if text else 0})

        # Step 3: Generate unique filename
        logger.info("Step 3: Generating unique filename")
        resolved_filename = generate_unique_filename(self.db, user_id, filename)
        logger.info("Step 3: Filename resolved", extra={"resume_filename": resolved_filename})

        logger.info(
            "Creating resume",
            extra={
                "user_id": str(user_id),
                "resume_filename": resolved_filename,
                "size": len(content),
            },
        )

        # Step 4: DB create
        logger.info("Step 4: Creating DB record")
        try:
            resume = self.repo.create(
                id=uuid.uuid4(),
                user_id=user_id,
                filename=resolved_filename,
                pdf_data=content,
                extracted_text=text,
            )
            logger.info("Step 4: DB record created", extra={"resume_id": str(resume.id)})
            return resume
        except Exception as e:
            logger.error("Step 4: DB create failed", exc_info=True, extra={"error": str(e)})
            raise

    def list_by_user(self, user_id: uuid.UUID) -> list[models.Resume]:
        """List all resumes for a user."""
        return self.repo.get_by_user(user_id)

    def get_for_user(self, user_id: uuid.UUID, resume_id: uuid.UUID) -> models.Resume:
        """Get a specific resume for a user."""
        resume = self.repo.get_by_user_and_id(user_id, resume_id)
        if not resume:
            raise NotFoundError("Resume", str(resume_id))
        return resume

    def delete_for_user(self, user_id: uuid.UUID, resume_id: uuid.UUID) -> bool:
        """Delete a resume for a user."""
        logger.info(
            "Deleting resume",
            extra={"user_id": str(user_id), "resume_id": str(resume_id)},
        )
        return self.repo.delete_by_user_and_id(user_id, resume_id)

    def count_for_user(self, user_id: uuid.UUID) -> int:
        """Count resumes for a user."""
        return self.repo.count_by_user(user_id)