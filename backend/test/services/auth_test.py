import os
from typing import Any
import pytest
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from jose import jwt
from datetime import timedelta
from backend.services.auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    authenticate_user,
    get_current_user
)
from backend.services.exceptions import UserNotFoundException
from backend.services.user import UserService
from .user_data import user

# Data Setup and Injected Service Fixtures
from .core_data import setup_insert_data_fixture
from .fixtures import  add_test_user

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET")
if not SECRET_KEY:
    raise ValueError("JWT_SECRET environment variable is not set")

ALGORITHM = "HS256"

@pytest.fixture
def user_service(session: Session):
    return UserService(session)

@pytest.fixture
def add_test_user(user_service: UserService):
    user_service.create_user(user)
    yield

def test_verify_password():
    hashed_password = get_password_hash("testpassword")
    assert verify_password("testpassword", hashed_password)
    assert not verify_password("wrongpassword", hashed_password)

def test_create_access_token():
    data = {"sub": "sally@gmail.com"}
    expires_delta = timedelta(minutes=15)
    token = create_access_token(data, expires_delta)
    decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded_data["sub"] == "sally@gmail.com"
    assert "exp" in decoded_data

def test_authenticate_user(session: Session):
    authenticated_user = authenticate_user(session, "sally@gmail.com", "studentspassword")
    assert authenticated_user.email == user.email
    assert authenticated_user.first_name == user.first_name

def test_authenticate_user_invalid(session: Session):
    with pytest.raises(UserNotFoundException):
        authenticate_user(session, "invalid@gmail.com", "studentspassword")

def test_get_current_user(session: Session):
    data = {"sub": "sally@gmail.com"}
    token = create_access_token(data, timedelta(minutes=15))
    current_user = get_current_user(session, token)
    assert current_user.email == user.email
    assert current_user.first_name == user.first_name

def test_get_current_user_invalid_token(session: Session):
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(session, "invalidtoken")
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_current_user_expired_token(session: Session):
    data = {"sub": "sally@gmail.com"}
    expires_delta = timedelta(seconds=-1)
    token = create_access_token(data, expires_delta)
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(session, token)
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
