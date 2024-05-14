from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.services.tag import TagService
from ..models.tag import Tag, TagBase
from ..database import db_session

router = APIRouter(prefix="/api/tags", tags=["Tags"])

@router.post("", response_model=Tag)
def create_tag(tag_data: TagBase, db: Session = Depends(db_session)):
    tag_service = TagService(db)
    return tag_service.create_tag(tag_data)

@router.get("/{tag_id}", response_model=Tag)
def get_tag(tag_id: int, db: Session = Depends(db_session)):
    tag_service = TagService(db)
    return tag_service.get_tag(tag_id)

@router.get("", response_model=list[Tag])
def get_tags(db: Session = Depends(db_session)):
    tag_service = TagService(db)
    return tag_service.get_tags()

@router.put("/{tag_id}", response_model=Tag)
def update_tag(tag_id: int, tag_update: TagBase, db: Session = Depends(db_session)):
    tag_service = TagService(db)
    return tag_service.update_tag(tag_id, tag_update)

@router.delete("/{tag_id}")
def delete_tag(tag_id: int, db: Session = Depends(db_session)):
    tag_service = TagService(db)
    tag_service.delete_tag(tag_id)
    return {"message": "Tag deleted successfully"}
