# backend/entities/comment_entity.py
from datetime import datetime, timezone
from typing import Optional, Union
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base
from backend.models.comment import CommentCreate, CommentUpdate, CommentResponse

class CommentEntity(Base):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    description: Mapped[str] = mapped_column(String, nullable=False)
    post_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('projects.id'), nullable=True)
    discussion_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('discussions.id'), nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    user: Mapped['UserEntity'] = relationship('UserEntity')
    project: Mapped[Optional['ProjectEntity']] = relationship('ProjectEntity', back_populates='comments')
    discussion: Mapped[Optional['DiscussionEntity']] = relationship('DiscussionEntity', back_populates='comments')

    def to_comment_response(self):
        return CommentResponse(
            id=self.id,
            description=self.description,
            post_id=self.post_id,
            discussion_id=self.discussion_id,
            user_id=self.user_id,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    @staticmethod
    def from_model(comment: CommentCreate):
        return CommentEntity(
            description=comment.description,
            post_id=comment.post_id,
            discussion_id=comment.discussion_id,
            user_id=comment.user_id
        )
