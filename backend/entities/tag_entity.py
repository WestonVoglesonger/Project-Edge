from sqlalchemy import Column, Integer, String

from backend.models.tag import Tag
from .base import Base

class TagEntity(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)


    def to_model(self):
        return Tag(
            id=self.id,
            name=self.name,
        )

    @staticmethod
    def from_model(tag: Tag):
        return TagEntity(
            name=tag.name,
        )
