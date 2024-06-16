from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CommentCreate(BaseModel):
    description: str
    post_id: int
    user_id: int

class CommentUpdate(BaseModel):
    description: Optional[str] = None

class CommentResponse(BaseModel):
    id: int
    description: str
    post_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
