"""Mock data for users.

Three users are setup for testing and development purposes:

1. Rhonda Root (root user with all permissions)
2. Amy Ambassador (staff of XL with elevated permissions)
3. Sally Student (standard user without any special permissions)"""

import pytest
from sqlalchemy.orm import Session
from ...models.user import User
from ...entities.user_entity import UserEntity
from ...entities.user_role_table import user_role_table
from .reset_table_id_seq import reset_table_id_seq
from . import role_data

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


root = User(
        first_name="Rhonda",
        last_name="Root",
        email="root@gmail.com",
        password="rootpassword",
        accepted_community_agreement=True
    )

project_owner = User(
        first_name="Proj",
        last_name="Ector",
        email="proj@gmail.com",
        password="projpassword",
        accepted_community_agreement=True
    )

user = User(
        first_name="Sally",
        last_name="Student",
        email="user@gmail.com",
        password="studentpassword",
        accepted_community_agreement=True
    )

users = [root, project_owner, user]

roles_users = {
    role_data.root_role.id: [root],
    role_data.ambassador_role.id: [project_owner],
}


def insert_fake_data(session: Session):
    global users
    entities = []
    for user in users:
        entity = UserEntity.from_model(user)
        session.add(entity)
        entities.append(entity)
    reset_table_id_seq(session, UserEntity, UserEntity.id, len(users) + 1)
    session.commit()  # Commit to ensure User IDs in database

    # Associate Users with the Role(s) they are in
    for role_id, members in roles_users.items():
        for user in members:
            session.execute(
                user_role_table.insert().values(
                    {"role_id": role_id, "user_id": user.id}
                )
            )


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    insert_fake_data(session)
    session.commit()
    yield