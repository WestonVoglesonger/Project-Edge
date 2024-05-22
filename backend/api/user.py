from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from pydantic import ValidationError
from sqlalchemy.orm import Session
import os
import shutil

from backend.database import db_session
from backend.services.user import UserService
from ..models.user import ProfileForm, UserBase, UserResponse
from ..services.exceptions import UserNotFoundException, EmailAlreadyRegisteredException

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

@api.get("/{user_id}", response_model=UserResponse, tags=["Users"])
def read_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    try:
        return user_service.get_user(user_id=user_id)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@api.put("/{user_id}", response_model=UserResponse, tags=["Users"])
async def update_user(
    user_id: int,
    first_name: Optional[str] = Form(None),
    last_name: Optional[str] = Form(None),
    bio: Optional[str] = Form(None),
    email: Optional[str] = Form(...),
    accepted_community_agreement: Optional[bool] = Form(...),
    profile_picture: UploadFile = File(None),
    user_service: UserService = Depends(get_user_service)
):
    try:
        user_update_data = {
            "first_name": first_name,
            "last_name": last_name,
            "bio": bio,
            "email": email,
            "accepted_community_agreement": accepted_community_agreement,
            "profile_picture": None
        }

        # Handle the profile picture file
        if profile_picture:
            os.makedirs('files', exist_ok=True)
            file_location = f"files/{user_id}_profile_picture.png"
            with open(file_location, "wb+") as file_object:
                shutil.copyfileobj(profile_picture.file, file_object)
            user_update_data["profile_picture"] = file_location

        # Ensure required fields are provided
        if not email:
            raise HTTPException(status_code=400, detail="Email is required")
        if accepted_community_agreement is None:
            raise HTTPException(status_code=400, detail="Accepted Community Agreement is required")

        # Remove None values from the user_update_data dictionary
        user_update_data = {k: v for k, v in user_update_data.items() if v is not None}

        # Create the ProfileForm object
        user_update = ProfileForm(**user_update_data)

        return user_service.update_user(user_id=user_id, user_update=user_update)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
