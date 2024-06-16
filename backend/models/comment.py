# backend/models/comment.py
from pydantic import BaseModel, Field, root_validator
from datetime import datetime
from typing import Optional

class CommentCreate(BaseModel):
    description: str
    project_id: Optional[int] = None
    discussion_id: Optional[int] = None
    user_id: int

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
