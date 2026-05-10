"""Pydantic schemas for job description endpoints."""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class JobCreatePayload(BaseModel):
    title: str = Field(..., min_length=2, description="Job title or position name")
    description: str = Field(..., min_length=20, description="Full job description text")


class JobResponse(BaseModel):
    id: str
    title: str
    description_text: str
    uploaded_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @field_validator('id', mode='before')
    @classmethod
    def convert_uuid(cls, v):
        if isinstance(v, UUID):
            return str(v)
        return v


class JobListResponse(BaseModel):
    jobs: list[JobResponse]

    model_config = ConfigDict(from_attributes=True)
