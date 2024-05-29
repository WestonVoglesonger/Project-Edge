from typing import List
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from ..models.user import ProfileForm, User, UserBase, UserResponse

association_table_current_users = Table(
    'association_current_users', Base.metadata,
    Column('project_id', ForeignKey('projects.id'), primary_key=True),
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    extend_existing=True
)

association_table_owners = Table(
    'association_owners', Base.metadata,
    Column('project_id', ForeignKey('projects.id'), primary_key=True),
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    extend_existing=True
)

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

    projects_as_user: Mapped[List['ProjectEntity']] = relationship(
        'ProjectEntity', secondary=association_table_current_users, back_populates='current_users')
    projects_as_owner: Mapped[List['ProjectEntity']] = relationship(
        'ProjectEntity', secondary=association_table_owners, back_populates='owners')

    def to_user_response(self):
        return UserResponse(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            accepted_community_agreement=self.accepted_community_agreement,
            bio=self.bio,
            profile_picture=self.profile_picture,
        )

    def to_user(self):
        return User(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            password=self.hashed_password,
            accepted_community_agreement=self.accepted_community_agreement,
            bio=self.bio,
            profile_picture=self.profile_picture,
        )

    @staticmethod
    def from_existing_model(user: User):
        return UserEntity(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            hashed_password=user.hash_password(),
            accepted_community_agreement=user.accepted_community_agreement,
            bio=user.bio,
            profile_picture=user.profile_picture,
        )

    @staticmethod
    def from_new_model(user: UserBase, hashed_password: str):
        return UserEntity(
            first_name=None,
            last_name=None,
            email=user.email,
            hashed_password=hashed_password,
            accepted_community_agreement=user.accepted_community_agreement,
            bio=None,
            profile_picture=None,
        )
