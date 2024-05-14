from pydantic import BaseModel, EmailStr
from typing import Optional

class UserIdentity(BaseModel):
    id: Optional[int] = None

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    accepted_community_agreement: bool = False

class User(UserIdentity, BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    accepted_community_agreement: bool = False

class ProfileForm(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    accepted_community_agreement: bool = False
