from sqlalchemy.orm import Session

from backend.entities.tag_entity import TagEntity
from ..models.tag import Tag, TagBase

class TagService:
    def __init__(self, db: Session):
        self.db = db

    def create_tag(self, tag_data: TagBase) -> Tag:
        existing_tag = self.db.query(TagEntity).filter(TagEntity.name == tag_data.name).first()
        if existing_tag:
            raise ValueError("Tag with this name already exists")
        tag_entity = TagEntity.from_model(tag_data)
        self.db.add(tag_entity)
        self.db.commit()
        self.db.refresh(tag_entity)
        return tag_entity.to_model()

    def get_tag(self, tag_id: int) -> Tag:
        tag_entity = self.db.query(TagEntity).filter(TagEntity.id == tag_id).first()
        if tag_entity is None:
            raise ValueError("Tag not found")
        return tag_entity.to_model()

    def get_tags(self) -> list[Tag]:
        tag_entities = self.db.query(TagEntity).all()
        return [tag_entity.to_model() for tag_entity in tag_entities]

    def update_tag(self, tag_id: int, tag_update: TagBase) -> Tag:
        tag_entity = self.db.query(TagEntity).filter(TagEntity.id == tag_id).first()
        if tag_entity is None:
            raise ValueError("Tag not found")
        tag_entity.name = tag_update.name
        self.db.commit()
        self.db.refresh(tag_entity)
        return tag_entity.to_model()

    def delete_tag(self, tag_id: int) -> None:
        tag_entity = self.db.query(TagEntity).filter(TagEntity.id == tag_id).first()
        if tag_entity is None:
            raise ValueError("Tag not found")
        self.db.delete(tag_entity)
        self.db.commit()
