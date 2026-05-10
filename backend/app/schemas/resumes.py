"""Pydantic schemas for resume endpoints."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator


class ResumeResponse(BaseModel):
    id: str
    filename: str
    uploaded_at: datetime
    extracted_text: str | None = None

    model_config = ConfigDict(from_attributes=True)

    @field_validator('id', mode='before')
    @classmethod
    def convert_uuid(cls, v):
        if isinstance(v, UUID):
            return str(v)
        return v


class ResumeListResponse(BaseModel):
    resumes: list[ResumeResponse]

    model_config = ConfigDict(from_attributes=True)
