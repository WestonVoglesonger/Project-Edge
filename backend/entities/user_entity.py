from sqlalchemy import Column, Integer, String, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.entities.tag_entity import TagEntity
from .base import Base
from .user_tag_association import user_tag_association
from ..models.user import ProfileForm, User, UserBase

class UserEntity(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    accepted_community_agreement: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    bio: Mapped[Text] = mapped_column(Text, nullable=True)
    profile_picture: Mapped[str] = mapped_column(String, nullable=True)
    areas_of_interest = relationship("TagEntity", secondary=user_tag_association)

    def to_model(self):
        return User(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            password=self.hashed_password,
            accepted_community_agreement=self.accepted_community_agreement,
            bio=self.bio,
            profile_picture=self.profile_picture,
            areas_of_interest=[tag.id for tag in self.areas_of_interest]
        )

    @staticmethod
    def from_model(user: ProfileForm, hashed_password: str):
        return UserEntity(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            hashed_password=hashed_password,
            accepted_community_agreement=user.accepted_community_agreement,
            bio=user.bio,
            profile_picture=user.profile_picture,
            areas_of_interest=[TagEntity(id=tag_id) for tag_id in user.areas_of_interest] if user.areas_of_interest else []
        )
