import logging
import traceback
from fastapi import APIRouter, Depends, HTTPException, Form, Query
from pydantic import ValidationError
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.database import db_session
from backend.services.user import UserService
from ..models.user import ProfileForm, UserBase, UserIDs, UserResponse
from ..services.exceptions import UserNotFoundException, EmailAlreadyRegisteredException
from ..services.auth import get_current_user

logger = logging.getLogger(__name__)

api = APIRouter(prefix="/api/user")
openapi_tags = {
    "name": "Users",
    "description": "User profile search and related operations.",
}

def get_user_service(db: Session = Depends(db_session)) -> UserService:
    return UserService(db)

@api.post("", response_model=UserResponse, tags=["Users"])
def create_user(user: UserBase, user_service: UserService = Depends(get_user_service)):
    try:
        return user_service.create_user(user)
    except EmailAlreadyRegisteredException as e:
        raise HTTPException(status_code=400, detail=str(e))

@api.get("/search", response_model=List[UserResponse], tags=["Users"])
def search_users(name: str = Query(...), user_service: UserService = Depends(get_user_service), current_user: UserResponse = Depends(get_current_user)):
    """Retrieve users by name."""
    try:
        users = user_service.search_users_by_name(name)
        return users
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Error processing query: {str(e)}")

@api.get("/{user_id}", response_model=UserResponse, tags=["Users"])
def read_user(user_id: int, user_service: UserService = Depends(get_user_service), current_user: UserResponse = Depends(get_current_user)):
    """Retrieve a user by their user ID."""
    try:
        return user_service.get_user(user_id=user_id)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@api.post("/getByIds", response_model=List[UserResponse], tags=["Users"])
def get_users_by_ids(user_ids: UserIDs, user_service: UserService = Depends(get_user_service), current_user: UserResponse = Depends(get_current_user)):
    logger.info(f"Received user IDs: {user_ids.ids}")
    if not user_ids.ids:
        logger.error("No user IDs provided.")
        raise HTTPException(status_code=400, detail="No user IDs provided.")
    try:
        users = user_service.get_users_by_ids(user_ids.ids)
        if not users:
            raise UserNotFoundException("No users found with the given IDs")
        return users
    except UserNotFoundException as e:
        logger.error(f"UserNotFoundException: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@api.put("/{user_id}", response_model=UserResponse, tags=["Users"])
async def update_user(
    user_id: int,
    first_name: Optional[str] = Form(None),
    last_name: Optional[str] = Form(None),
    bio: Optional[str] = Form(None),
    email: str = Form(...),
    accepted_community_agreement: bool = Form(...),
    user_service: UserService = Depends(get_user_service),
    current_user: UserResponse = Depends(get_current_user)
):
    try:
        user_update_data = {
            "first_name": first_name,
            "last_name": last_name,
            "bio": bio,
            "email": email,
            "accepted_community_agreement": accepted_community_agreement
        }

        user_update_data = {k: v for k, v in user_update_data.items() if v is not None}

        user_update = ProfileForm(**user_update_data)

        return user_service.update_user(user_id=user_id, user_update=user_update)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@api.delete("/{user_id}", response_model=UserResponse, tags=["Users"])
def delete_user(user_id: int, user_service: UserService = Depends(get_user_service), current_user: UserResponse = Depends(get_current_user)):
    """Delete a user from the system."""
    try:
        return user_service.delete_user(user_id=user_id)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
