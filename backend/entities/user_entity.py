from sqlalchemy import Integer, String, Boolean, Text
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from backend.models.user import User, UserBase

Base = declarative_base()

class UserEntity(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    accepted_community_agreement: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    bio: Mapped[str] = mapped_column(Text, nullable=True)
    profile_picture: Mapped[str] = mapped_column(String, nullable=True)
    areas_of_interest: Mapped[str] = mapped_column(String, nullable=True)

    def to_model(self):
        return User(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            accepted_community_agreement=self.accepted_community_agreement,
            bio=self.bio,
            profile_picture=self.profile_picture,
            areas_of_interest=self.areas_of_interest
        )

    @staticmethod
    def from_model(user: 'UserBase', hashed_password: str):
        return UserEntity(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            hashed_password=hashed_password,
            accepted_community_agreement=user.accepted_community_agreement,
            bio=user.bio,
            profile_picture=user.profile_picture,
            areas_of_interest=user.areas_of_interest
        )
