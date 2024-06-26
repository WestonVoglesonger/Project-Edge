from pydantic import BaseModel, EmailStr
from typing import List, Optional
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserIdentity(BaseModel):
    id: Optional[int] = None

class UserBase(UserIdentity):
    email: EmailStr
    password: str
    accepted_community_agreement: bool = False

    def hash_password(self):
        return pwd_context.hash(self.password)

class ProfileForm(BaseModel):
    id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    email: EmailStr
    password: Optional[str] = None
    accepted_community_agreement: bool
    
    def hash_password(self):
        return pwd_context.hash(self.password)

class UserResponse(BaseModel):
    id: Optional[int]
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr
    accepted_community_agreement: bool
    bio: Optional[str] = None
    profile_picture: Optional[str] = None

class User(UserBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    profile_picture: Optional[str] = None

    def to_user_response(self) -> UserResponse:
        return UserResponse(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            accepted_community_agreement=self.accepted_community_agreement,
            bio=self.bio,
            profile_picture=self.profile_picture
        )