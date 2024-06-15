# backend/entities/discussion_entity.py
from datetime import datetime, timezone
from typing import List
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base
from backend.models.discussion import DiscussionCreate, DiscussionUpdate, DiscussionResponse
from backend.entities.user_entity import UserEntity

association_table_discussion_participants = Table(
    'association_discussion_participants', Base.metadata,
    Column('discussion_id', ForeignKey('discussions.id'), primary_key=True),
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    extend_existing=True
)

class DiscussionEntity(Base):
    __tablename__ = 'discussions'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    participants: Mapped[List[UserEntity]] = relationship('UserEntity', secondary=association_table_discussion_participants, back_populates='discussions')

    def to_discussion_response(self):
        return DiscussionResponse(
            id=self.id,
            title=self.title,
            description=self.description,
            created_at=self.created_at,
            updated_at=self.updated_at,
            user_id=self.user_id,
            participants=[participant.to_user_response() for participant in self.participants]
        )

    @staticmethod
    def from_model(discussion: DiscussionCreate, participants: List[UserEntity]):
        return DiscussionEntity(
            title=discussion.title,
            description=discussion.description,
            user_id=discussion.user_id,
            participants=participants
        )
