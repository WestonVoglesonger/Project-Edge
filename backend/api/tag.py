from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.models.tag import Tag, TagBase, TagCreate
from backend.exceptions import TagNotFoundException
from backend.database import db_session
from backend.services.tag import TagService

api = APIRouter(prefix="/api/tags")
openapi_tags = {
    "name": "Tags",
    "description": "Operations related to tags.",
}

@api.post("", response_model=Tag, tags=["Tags"])
def create_tag(tag_data: TagBase, tag_service: TagService = Depends()):
    """Create a new tag in the system."""
    return tag_service.create_tag(tag_data)

@api.get("/{tag_id}", response_model=Tag, tags=["Tags"])
def read_tag(tag_id: int, tag_service: TagService = Depends()):
    """Retrieve a tag by its ID."""
    try:
        return tag_service.get_tag(tag_id)
    except TagNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@api.delete("/{tag_id}", response_model=Tag, tags=["Tags"])
def delete_tag(tag_id: int, tag_service: TagService = Depends()):
    """Delete a tag from the system."""
    try:
        return tag_service.delete_tag(tag_id)
    except TagNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
