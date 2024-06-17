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
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey('projects.id'), nullable=True)
    discussion_id: Mapped[int] = mapped_column(Integer, ForeignKey('discussions.id'), nullable=True)
    parent_id: Mapped[int] = mapped_column(Integer, ForeignKey('comments.id'), nullable=True)

    author = relationship("UserEntity", back_populates="comments")
    project = relationship("ProjectEntity", back_populates="comments")
    discussion = relationship("DiscussionEntity", back_populates="comments")
    parent = relationship("CommentEntity", remote_side=[id], back_populates="replies")
    replies = relationship("CommentEntity", back_populates="parent", cascade="all, delete-orphan", single_parent=True)

    def to_comment_response(self):
        return CommentResponse(
            id=self.id,
            description=self.description,
            created_at=self.created_at,
            updated_at=self.updated_at,
            author=self.author.to_user_response(),
            project_id=self.project_id,
            discussion_id=self.discussion_id,
            parent_id=self.parent_id,
            replies=[reply.to_comment_response() for reply in self.replies]
        )

    @staticmethod
    def from_model(comment: CommentCreate):
        return CommentEntity(
            description=comment.description,
            author_id=comment.author_id,
            project_id=comment.project_id,
            discussion_id=comment.discussion_id,
            parent_id=comment.parent_id
        )