from datetime import datetime, timezone
from typing import List
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base
from backend.models.discussion import DiscussionCreate, DiscussionUpdate, DiscussionResponse

class DiscussionEntity(Base):
    __tablename__ = 'discussions'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=True)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    author: Mapped['UserEntity'] = relationship(back_populates='authored_discussions')

    comments = relationship("CommentEntity", back_populates="discussion", cascade="all, delete-orphan")

    def to_discussion_response(self):
        return DiscussionResponse(
            id=self.id,
            title=self.title,
            description=self.description,
            created_at=self.created_at,
            updated_at=self.updated_at,
            author_id=self.author_id
        )

    @staticmethod
    def from_model(discussion: DiscussionCreate):
        return DiscussionEntity(
            title=discussion.title,
            description=discussion.description,
            author_id=discussion.author_id
        )
