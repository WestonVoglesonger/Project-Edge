import pytest
from sqlalchemy.orm import Session
from backend.models.user import ProfileForm, UserBase
from backend.entities.user_entity import UserEntity
from .reset_table_id_seq import reset_table_id_seq

__authors__ = ["Weston Voglesonger"]
__copyright__ = ["Copyright 2023"]
__license__ = "MIT"

user = ProfileForm(
    id=1,
    first_name="Sally",
    last_name="Student",
    bio="I am a student at the University of North Carolina.",
    profile_picture="https://example.com/profile.jpg",
    email="sally@gmail.com",
    password="studentspassword",
    accepted_community_agreement=True
)

new_user = UserBase(
    email="testuser@example.com",
    password="testpassword",
    accepted_community_agreement=True
)

update_data = ProfileForm(
    first_name="Sallie",
    last_name="Students",
    email="users@gmail.com",
    password="studentspassword",
    accepted_community_agreement=True
)

users = [user]

def insert_fake_data(session: Session):
    global users
    entities = []
    for user in users:
        entity = UserEntity.from_model(user, user.hash_password())
        session.add(entity)
        entities.append(entity)
    session.commit()  # Commit to ensure User IDs in database
    reset_table_id_seq(session, UserEntity, UserEntity.id, len(users) + 1)

@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    insert_fake_data(session)
    session.commit()
    yield
