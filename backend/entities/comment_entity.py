from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from backend.models.comment import CommentCreate, CommentResponse
from .base import Base

class CommentEntity(Base):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    description: Mapped[str] = mapped_column(String, nullable=False)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('posts.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=True)

    def to_comment_response(self):
        return CommentResponse(
            id=self.id,
            description=self.description,
            post_id=self.post_id,
            user_id=self.user_id,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    @staticmethod
    def from_model(comment: CommentCreate):
        return CommentEntity(
            description=comment.description,
            post_id=comment.post_id,
            user_id=comment.user_id
        )
