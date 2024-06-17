from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class CommentCreate(BaseModel):
    description: str
    project_id: Optional[int] = None
    discussion_id: Optional[int] = None
    user_id: int
    parent_id: Optional[int] = None


class CommentUpdate(BaseModel):
    description: Optional[str] = None

class CommentResponse(BaseModel):
    id: int
    description: str
    project_id: Optional[int] = None
    discussion_id: Optional[int] = None
    user_id: int
    created_at: datetime
    updated_at: datetime
    parent_id: Optional[int] = None
    replies: List["CommentResponse"] = []
