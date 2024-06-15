from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from backend.models.user import UserResponse

class DiscussionIdentity(BaseModel):
    id: int

class DiscussionCreate(BaseModel):
    title: str
    description: str
    user_id: int

class DiscussionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class DiscussionResponse(DiscussionIdentity):
    title: str
    description: str
    created_at: datetime
    updated_at: datetime
    user_id: int
    participants: List[UserResponse]
