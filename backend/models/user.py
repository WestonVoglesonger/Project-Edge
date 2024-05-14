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

class User(UserBase, UserIdentity):
    pass

class ProfileForm(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    accepted_community_agreement: bool = False
