from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base

from backend.models.user import User, UserBase

Base = declarative_base()

class UserEntity(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    accepted_community_agreement = Column(Boolean, default=False, nullable=False)

    def to_model(self):
        return User(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            accepted_community_agreement=self.accepted_community_agreement
        )

    @staticmethod
    def from_model(user: 'UserBase', hashed_password: str):
        return UserEntity(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            hashed_password=hashed_password,
            accepted_community_agreement=user.accepted_community_agreement
        )
