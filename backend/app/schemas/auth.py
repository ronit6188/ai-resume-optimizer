"""Pydantic schemas for authentication endpoints."""

from __future__ import annotations

import re

from pydantic import BaseModel, Field, field_validator


class SignupPayload(BaseModel):
    email: str = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="Plain-text password")

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        normalized = value.strip().lower()
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", normalized):
            raise ValueError("Enter a valid email address")
        return normalized


class TokenResponse(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
