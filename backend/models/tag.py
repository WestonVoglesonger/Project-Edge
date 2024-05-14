# backend/models/tag.py
from pydantic import BaseModel

class TagBase(BaseModel):
    name: str

class Tag(TagBase):
    id: int

