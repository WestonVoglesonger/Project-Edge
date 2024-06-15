# discussions_entity.py

from typing import List
from sqlalchemy import Column, Integer, String, Table, ForeignKey
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
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    author: Mapped[UserEntity] = relationship('UserEntity', back_populates='authored_discussions')
    participants: Mapped[List[UserEntity]] = relationship('UserEntity', secondary=association_table_discussion_participants, back_populates='participating_discussions')

    def to_discussion_response(self):
        return DiscussionResponse(
            id=self.id,
            title=self.title,
            description=self.description,
            author=self.author.to_user_response(),
            participants=[participant.to_user_response() for participant in self.participants]
        )

    @staticmethod
    def from_model(discussion: DiscussionCreate, author: UserEntity, participants: List[UserEntity]):
        return DiscussionEntity(
            title=discussion.title,
            description=discussion.description,
            author=author,
            participants=participants
        )
