from sqlalchemy.orm import Session
from ..models.tag import Tag, TagBase, TagCreate
from ..entities.tag_entity import TagEntity
from ..exceptions import TagNotFoundException

class TagService:
    def __init__(self, db: Session):
        self.db = db

    def get_tag(self, tag_id: int) -> Tag:
        tag_entity = self.db.query(TagEntity).filter(TagEntity.id == tag_id).first()
        if tag_entity is None:
            raise TagNotFoundException(f"Tag with id {tag_id} not found")
        return tag_entity.to_model()

    def create_tag(self, tag_data: TagBase) -> Tag:
        tag_entity = TagEntity(name=tag_data.name)
        self.db.add(tag_entity)
        self.db.commit()
        self.db.refresh(tag_entity)
        return tag_entity.to_model()

    def delete_tag(self, tag_id: int):
        tag_entity = self.db.query(TagEntity).filter(TagEntity.id == tag_id).first()
        if tag_entity is None:
            raise TagNotFoundException(f"Tag with id {tag_id} not found")
        self.db.delete(tag_entity)
        self.db.commit()
