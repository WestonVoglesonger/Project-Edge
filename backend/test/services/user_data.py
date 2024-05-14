"""Mock data for users.

Three users are setup for testing and development purposes:

1. Rhonda Root (root user with all permissions)
2. Amy Ambassador (staff of XL with elevated permissions)
3. Sally Student (standard user without any special permissions)"""

import pytest
from sqlalchemy.orm import Session
from ...models.user import ProfileForm, User, UserBase
from ...entities.user_entity import UserEntity
from .reset_table_id_seq import reset_table_id_seq

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


root = User(
        id=1,
        first_name="Rhonda",
        last_name="Root",
        email="root@gmail.com",
        password="rootpassword",
        accepted_community_agreement=True
    )

project_owner = User(
        id=2,
        first_name="Proj",
        last_name="Ector",
        email="proj@gmail.com",
        password="projpassword",
        accepted_community_agreement=True
    )

user = User(
        id=3,
        first_name="Sally",
        last_name="Student",
        email="user@gmail.com",
        password="studentpassword",
        accepted_community_agreement=True
    )

new_user = ProfileForm(
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

users = [root, project_owner, user]


def insert_fake_data(session: Session):
    global users
    entities = []
    for user in users:
        entity = UserEntity.from_model(user, user.hash_password())
        session.add(entity)
        entities.append(entity)
    reset_table_id_seq(session, UserEntity, UserEntity.id, len(users) + 1)
    session.commit()  # Commit to ensure User IDs in database

@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    insert_fake_data(session)
    session.commit()
    yield