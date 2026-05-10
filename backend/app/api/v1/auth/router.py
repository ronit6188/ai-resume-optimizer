"""Authentication routes."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core import security
from app.core.config import settings
from app.db import models
from app.db.session import get_db
from app.schemas.auth import SignupPayload, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])


def _set_auth_cookies(response: Response, access: str, refresh: str) -> None:
    is_prod = settings.ENV == "prod"
    response.set_cookie(
        key="access_token",
        value=access,
        httponly=True,
        secure=is_prod,
        samesite="strict" if is_prod else "lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh,
        httponly=True,
        secure=is_prod,
        samesite="strict" if is_prod else "lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600,
        path="/",
    )


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def signup(payload: SignupPayload, response: Response, db: Session = Depends(get_db)) -> TokenResponse:
    existing = db.execute(select(models.User).where(models.User.email == payload.email)).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = models.User(
        id=uuid.uuid4(),
        email=payload.email.lower().strip(),
        password_hash=security.hash_password(payload.password),
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    access = security.create_access_token(str(user.id))
    refresh = security.create_refresh_token(str(user.id))
    _set_auth_cookies(response, access, refresh)
    return TokenResponse(access_token=access, refresh_token=refresh)


@router.post("/login", response_model=TokenResponse)
def login(
    response: Response,
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> TokenResponse:
    user = db.execute(select(models.User).where(models.User.email == form.username.lower())).scalar_one_or_none()
    if not user or not security.verify_password(form.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is not active")

    access = security.create_access_token(str(user.id))
    refresh = security.create_refresh_token(str(user.id))
    _set_auth_cookies(response, access, refresh)
    return TokenResponse(access_token=access, refresh_token=refresh)


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(request: Request, response: Response, db: Session = Depends(get_db)) -> TokenResponse:
    refresh = request.cookies.get("refresh_token")
    if not refresh:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    payload = security.decode_token(refresh)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user_uuid = uuid.UUID(payload["sub"])
    user = db.execute(select(models.User).where(models.User.id == user_uuid)).scalar_one_or_none()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access = security.create_access_token(str(user.id))
    new_refresh = security.create_refresh_token(str(user.id))
    _set_auth_cookies(response, new_access, new_refresh)
    return TokenResponse(access_token=new_access, refresh_token=new_refresh)


@router.get("/me")
def me(user=Depends(security.get_current_user), db: Session = Depends(get_db)) -> dict[str, str]:
    current_uuid = uuid.UUID(user["sub"])
    current = db.execute(select(models.User).where(models.User.id == current_uuid)).scalar_one_or_none()
    if not current:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": str(current.id), "email": current.email}


@router.post("/logout")
def logout(response: Response) -> dict[str, str]:
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"detail": "Logged out"}