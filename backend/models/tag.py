from pydantic import BaseModel
from typing import Optional

class TagBase(BaseModel):
    name: str

class Tag(TagBase):
    id: Optional[int] = None
