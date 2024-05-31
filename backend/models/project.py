from pydantic import BaseModel
from typing import List, Optional

from backend.models.user import UserResponse

class ProjectIdentity(BaseModel):
    id: int

class Project(ProjectIdentity):
    name: str
    description: str
    team_members: List[UserResponse]
    project_leaders: List[UserResponse]

class ProjectCreate(BaseModel):
    name: str
    description: str
    team_members: Optional[List[UserResponse]] = None
    project_leaders: Optional[List[UserResponse]] = None

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    team_members: Optional[List[UserResponse]] = None
    project_leaders: Optional[List[UserResponse]] = None

class ProjectResponse(ProjectIdentity):
    name: str
    description: str
    team_members: List[UserResponse]
    project_leaders: List[UserResponse]

