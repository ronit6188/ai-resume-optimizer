"""Utility functions for validating uploads."""

from __future__ import annotations

from fastapi import HTTPException, UploadFile, status

MAX_PDF_SIZE = 5 * 1024 * 1024


def validate_pdf(file: UploadFile) -> None:
    """Raise HTTPException if the upload does not look like a PDF."""
    if file.content_type not in {"application/pdf", "application/octet-stream"}:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Only PDF files are accepted",
        )

    if file.headers.get("content-length"):
        size = int(file.headers["content-length"])
        if size > MAX_PDF_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="PDF size exceeds 5 MiB limit",
            )

    head = file.file.read(5)
    file.file.seek(0)
    if head != b"%PDF-":
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Uploaded file is not a valid PDF",
        )


def validate_pdf_by_content(content: bytes) -> None:
    """Validate PDF content directly (bytes)."""
    if len(content) > MAX_PDF_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="PDF size exceeds 5 MiB limit",
        )

    if len(content) < 5:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Invalid PDF content",
        )

    if content[:5] != b"%PDF-":
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Uploaded file is not a valid PDF",
        )
