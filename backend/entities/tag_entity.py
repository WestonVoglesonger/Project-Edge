from pydantic import Tag
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from backend.models.tag import TagBase

Base = declarative_base()

class TagEntity(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)

    def to_model(self):
        return Tag(
            id=self.id,
            name=self.name
        )

    @staticmethod
    def from_model(tag: 'TagBase'):
        return TagEntity(
            name=tag.name
        )
