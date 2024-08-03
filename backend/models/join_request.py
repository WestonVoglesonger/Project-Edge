from pydantic import BaseModel
from datetime import datetime

class JoinRequestCreate(BaseModel):
    user_id: int
    project_id: int

class JoinRequestResponse(BaseModel):
    id: int
    user_id: int
    project_id: int
    created_at: datetime
    status: int
