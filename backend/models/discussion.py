from pydantic import BaseModel
from typing import List, Optional

from backend.models.user import UserResponse

class DiscussionIdentity(BaseModel):
    id: int

class Discussion(DiscussionIdentity):
    title: str
    description: str
    participants: List[UserResponse]
    author: UserResponse

class DiscussionCreate(BaseModel):
    title: str
    description: str
    participants: Optional[List[UserResponse]] = None
    author: UserResponse

class DiscussionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    participants: Optional[List[UserResponse]] = None

class DiscussionResponse(DiscussionIdentity):
    title: str
    description: str
    participants: List[UserResponse]
    author: UserResponse
