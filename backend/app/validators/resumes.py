"""Input validators for requests."""

from __future__ import annotations

import uuid
from typing import Any

from app.exceptions import ValidationError


def validate_uuid(value: str, field_name: str = "id") -> uuid.UUID:
    """Validate UUID string."""
    try:
        return uuid.UUID(value)
    except ValueError:
        raise ValidationError(f"Invalid {field_name} format", details={"field": field_name})


def validate_required_string(value: str | None, field_name: str, min_length: int = 1) -> str:
    """Validate required string field."""
    if not value:
        raise ValidationError(f"{field_name} is required", details={"field": field_name})
    if not value.strip():
        raise ValidationError(f"{field_name} cannot be empty", details={"field": field_name})
    if len(value.strip()) < min_length:
        raise ValidationError(
            f"{field_name} must be at least {min_length} characters",
            details={"field": field_name},
        )
    return value.strip()


def validate_optional_string(value: str | None, field_name: str) -> str | None:
    """Validate optional string field."""
    if value is None:
        return None
    return value.strip() if value.strip() else None


class ResumeValidator:
    """Validator for resume operations."""

    @staticmethod
    def validate_filename(filename: str | None) -> str:
        """Validate and sanitize filename."""
        if not filename:
            return "resume.pdf"

        filename = filename.strip()
        if not filename:
            return "resume.pdf"

        if len(filename) > 255:
            raise ValidationError("Filename too long", details={"field": "filename", "max": 255})

        if ".." in filename or "/" in filename or "\\" in filename:
            raise ValidationError("Invalid filename", details={"field": "filename"})

        return filename

    @staticmethod
    def validate_file_size(size: int, max_size: int = 5 * 1024 * 1024) -> None:
        """Validate file size."""
        if size > max_size:
            raise ValidationError(
                f"File size exceeds {max_size // (1024 * 1024)} MiB limit",
                details={"field": "file", "max_size": max_size},
            )


class JobValidator:
    """Validator for job description operations."""

    @staticmethod
    def validate_title(title: str | None) -> str:
        """Validate job title."""
        return validate_required_string(title, "title", min_length=2)

    @staticmethod
    def validate_description(description: str | None) -> str:
        """Validate job description."""
        return validate_required_string(description, "description", min_length=20)


class AnalysisValidator:
    """Validator for analysis operations."""

    @staticmethod
    def validate_resume_id(resume_id: str | None) -> uuid.UUID:
        """Validate resume ID."""
        if not resume_id:
            raise ValidationError("resume_id is required", details={"field": "resume_id"})
        return validate_uuid(resume_id, "resume_id")

    @staticmethod
    def validate_job_desc_id(job_desc_id: str | None) -> uuid.UUID | None:
        """Validate job description ID."""
        if not job_desc_id:
            return None
        return validate_uuid(job_desc_id, "job_desc_id")