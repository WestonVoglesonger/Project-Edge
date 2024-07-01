from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Integer, ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from backend.models.join_request import JoinRequestResponse
from .base import Base

class JoinRequestEntity(Base):
    __tablename__ = 'join_requests'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey('projects.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    status: Mapped[str] = mapped_column(String, default="pending", nullable=False)

    user = relationship('UserEntity', back_populates='join_requests')
    project = relationship('ProjectEntity', back_populates='join_requests')

    def to_join_request_response(self):
        return JoinRequestResponse(
            id=self.id,
            user_id=self.user_id,
            project_id=self.project_id,
            created_at=self.created_at,
            status=self.status
        )

    @staticmethod
    def from_model(user_id: int, project_id: int):
        return JoinRequestEntity(
            user_id=user_id,
            project_id=project_id
        )
