from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Dict

from backend.database import db_session
from backend.models.user import UserResponse
from backend.models.token import Token
from backend.services.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
    authenticate_user,
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
    get_current_user,
    get_user_by_email,
)

api = APIRouter(prefix="/api/auth")
openapi_tags = {
    "name": "Auth",
    "description": "Authorization related functions.",
}

@api.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(db_session),
) -> Dict[str, str]:
    """Authenticate user and return a JWT token."""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": user.email}, expires_delta=refresh_token_expires
    )
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@api.post("/refresh-token", response_model=Token)
def refresh_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(db_session),
) -> Dict[str, str]:
    """Refresh the access token using the refresh token."""
    user = get_user_by_email(db, form_data.username)
    if not user or not verify_refresh_token(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": user.email}, expires_delta=refresh_token_expires
    )
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@api.get("/users/me", response_model=UserResponse)
def read_users_me(
    current_user: UserResponse = Depends(get_current_user),
) -> UserResponse:
    """Retrieve the current authenticated user."""
    return current_user
