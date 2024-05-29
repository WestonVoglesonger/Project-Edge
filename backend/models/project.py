from pydantic import BaseModel
from typing import List, Optional

from backend.models.user import User, UserResponse

class ProjectIdentity(BaseModel):
    id: int

class Project(ProjectIdentity):
    name: str
    description: str
    current_users: List[User]
    owners: List[User]

class ProjectCreate(BaseModel):
    name: str
    description: str
    current_users: Optional[List[User]] = None
    owners: Optional[List[User]] = None

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    current_users: Optional[List[User]] = None
    owners: Optional[List[User]] = None

class ProjectResponse(ProjectIdentity):
    name: str
    description: str
    current_users: List[UserResponse]
    owners: List[UserResponse]

