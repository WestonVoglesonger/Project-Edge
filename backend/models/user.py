from pydantic import BaseModel, EmailStr
from typing import List, Optional
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserIdentity(BaseModel):
    id: Optional[int] = None

class UserBase(UserIdentity, BaseModel):
    email: EmailStr
    password: str
    accepted_community_agreement: bool = False

    def hash_password(self):
        return pwd_context.hash(self.password)

class User(UserBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    areas_of_interest: Optional[List[int]] = None

class ProfileForm(UserBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    areas_of_interest: Optional[List[int]] = None

class UserResponse(BaseModel):
    id: Optional[int]
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr
    accepted_community_agreement: bool
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    areas_of_interest: Optional[List[int]] = None
