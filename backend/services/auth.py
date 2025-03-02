import logging
import os
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from typing import Dict, Optional, Union, cast

from backend.database import db_session
from backend.entities.user_entity import UserEntity
from backend.models.user import UserResponse, User
from backend.services.exceptions import CredentialsException
from backend.services.user import UserService

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET")
if not SECRET_KEY:
    raise ValueError("JWT_SECRET environment variable is not set")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10080  # 7 days (increased from 24 hours)
REFRESH_TOKEN_EXPIRE_DAYS = 60  # 60 days (increased from 30 days)
TOKEN_LEEWAY_SECONDS = 86400  # 24 hours of leeway for clock skew and transition period

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
logger = logging.getLogger(__name__)

# Define oauth2_scheme once and reuse it
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user_service = UserService(db)
    user = user_service.get_user_by_email(username)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user


from backend.services.exceptions import (
    CredentialsException,
)  # Ensure this import is present


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(db_session)
) -> UserResponse:
    try:
        print(f"Received token: {token}")  # Log received token

        # First try with verification disabled to extract the payload
        try:
            # Get payload without verifying expiration
            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[ALGORITHM],
                options={"verify_exp": False},  # Don't verify expiration yet
            )

            # Now manually check expiration with extended grace period
            exp = payload.get("exp")
            if exp:
                token_expiry = datetime.fromtimestamp(exp, tz=timezone.utc)
                current_time = datetime.now(tz=timezone.utc)
                # Allow tokens expired within the last 24 hours
                if token_expiry < current_time - timedelta(hours=24):
                    logger.warning(
                        f"Token expired more than 24 hours ago: {token_expiry}"
                    )
                    raise CredentialsException()
                elif token_expiry < current_time:
                    logger.info(
                        f"Using expired token within grace period (expired: {token_expiry})"
                    )

            logger.info("Successfully decoded token with grace period handling")
        except JWTError as e:
            logger.warning(f"Token validation failed: {e}")
            raise CredentialsException()

        email = payload.get("sub")
        if email is None:
            logger.warning("Token missing 'sub' claim")
            raise CredentialsException()

        print(f"Decoded JWT payload: {payload}")  # Log the payload
    except JWTError as e:
        print(f"JWTError: {e}")
        raise CredentialsException()

    user = db.query(UserEntity).filter(UserEntity.email == email).first()
    if user is None:
        raise CredentialsException()
    print(f"Queried User: {user}")  # Log the user query result
    return user.to_user_response()


def create_access_token(
    data: Dict[str, str], expires_delta: Optional[timedelta] = None
) -> str:
    to_encode = cast(Dict[str, Union[str, int]], data.copy())
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": int(expire.timestamp())})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(
    data: Dict[str, str], expires_delta: Optional[timedelta] = None
) -> str:
    to_encode = cast(Dict[str, Union[str, int]], data.copy())
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({"exp": int(expire.timestamp())})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_refresh_token(token: str) -> Optional[Dict[str, str]]:
    try:
        # Get payload without verifying expiration
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"verify_exp": False},  # Don't verify expiration yet
        )

        # Now manually check expiration with extended grace period
        exp = payload.get("exp")
        if exp:
            token_expiry = datetime.fromtimestamp(exp, tz=timezone.utc)
            current_time = datetime.now(tz=timezone.utc)
            # For refresh tokens, use a 7-day grace period
            if token_expiry < current_time - timedelta(days=7):
                logger.warning(
                    f"Refresh token expired more than 7 days ago: {token_expiry}"
                )
                return None
            elif token_expiry < current_time:
                logger.info(
                    f"Using expired refresh token within grace period (expired: {token_expiry})"
                )

        return payload
    except JWTError as e:
        logger.warning(f"Refresh token validation failed: {e}")
        return None


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(UserEntity).filter(UserEntity.email == email).first()
