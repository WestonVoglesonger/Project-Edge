from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from backend.models.comment import CommentCreate, CommentUpdate, CommentResponse
from .base import Base

class CommentEntity(Base):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    description: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey('projects.id'), nullable=True)
    discussion_id: Mapped[int] = mapped_column(Integer, ForeignKey('discussions.id'), nullable=True)

    user = relationship("UserEntity", back_populates="comments")
    project = relationship("ProjectEntity", back_populates="comments")
    discussion = relationship("DiscussionEntity", back_populates="comments")

    def to_comment_response(self):
        return CommentResponse(
            id=self.id,
            description=self.description,
            created_at=self.created_at,
            updated_at=self.updated_at,
            user_id=self.user_id,
            project_id=self.project_id,
            discussion_id=self.discussion_id
        )

    @staticmethod
    def from_model(comment: CommentCreate):
        return CommentEntity(
            description=comment.description,
            user_id=comment.user_id,
            project_id=comment.project_id,
            discussion_id=comment.discussion_id
        )
