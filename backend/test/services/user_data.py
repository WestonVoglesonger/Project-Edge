import pytest
from sqlalchemy.orm import Session
from backend.models.user import User, UserBase, ProfileForm
from backend.entities.user_entity import UserEntity
from .reset_table_id_seq import reset_table_id_seq

user1 = User(
    id=1,
    first_name="Sally",
    last_name="Student",
    bio="I am a student at the University of North Carolina.",
    profile_picture="https://example.com/profile.jpg",
    email="sally@gmail.com",
    password="studentspassword",
    accepted_community_agreement=True
)

user2 = User(
    id=2,
    first_name="John",
    last_name="Doe",
    bio="I am a student at the University of North Carolina.",
    profile_picture="https://example.com/profile.jpg",
    email="john@gmail.com",
    password="johnspassword",
    accepted_community_agreement=True
)


new_user = UserBase(
    email="newuser@gmail.com",
    password="newpassword",
    accepted_community_agreement=True
)

update_data = ProfileForm(
    first_name="Updated",
    last_name="User",
    bio="Updated bio",
    profile_picture="https://example.com/updated_profile.jpg",
    email="updateduser@example.com",
    accepted_community_agreement=True
)

users = [user1, user2]

def insert_fake_data(session: Session):
    entities = []
    for user in users:
        hashed_password = user.hash_password()
        entity = UserEntity(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            hashed_password=hashed_password,
            accepted_community_agreement=user.accepted_community_agreement,
            bio=user.bio,
            profile_picture=user.profile_picture,
        )
        session.add(entity)
        entities.append(entity)
    session.commit()
    reset_table_id_seq(session, UserEntity, UserEntity.id, len(users) + 1)

@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    insert_fake_data(session)
    yield
