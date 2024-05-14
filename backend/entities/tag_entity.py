from sqlalchemy import Integer, String
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

from backend.models.tag import Tag

Base = declarative_base()

class TagEntity(Base):
    __tablename__ = 'tags'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

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
