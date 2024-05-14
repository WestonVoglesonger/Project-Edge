from pydantic import BaseModel, EmailStr
from typing import Optional
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserIdentity(BaseModel):
    id: Optional[int] = None

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    accepted_community_agreement: bool = False
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    areas_of_interest: Optional[str] = None


    def hash_password(self):
        return pwd_context.hash(self.password)

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

