from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..services import UserService
from ..models.user import User, UserBase, ProfileForm, UserResponse
from ..exceptions import UserNotFoundException, EmailAlreadyRegisteredException
from ..database import db_session

api = APIRouter(prefix="/api/user")
openapi_tags = {
    "name": "Users",
    "description": "User profile search and related operations.",
}

def get_user_service(db: Session = Depends(db_session)):
    return UserService(db)

@api.post("", response_model=UserResponse, tags=["Users"])
def create_user(user: ProfileForm, user_service: UserService = Depends(get_user_service)):
    """Create a new user in the system."""
    try:
        return user_service.create_user(user_data=user)
    except EmailAlreadyRegisteredException as e:
        raise HTTPException(status_code=400, detail=str(e))

@api.get("/{user_id}", response_model=UserResponse, tags=["Users"])
def read_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    """Retrieve a user by their user ID."""
    try:
        return user_service.get_user(user_id=user_id)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@api.put("/{user_id}", response_model=UserResponse, tags=["Users"])
def update_user(user_id: int, user: ProfileForm, user_service: UserService = Depends(get_user_service)):
    """Update an existing user's information."""
    try:
        return user_service.update_user(user_id=user_id, user_update=user)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@api.delete("/{user_id}", response_model=UserResponse, tags=["Users"])
def delete_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    """Delete a user from the system."""
    try:
        return user_service.delete_user(user_id=user_id)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
