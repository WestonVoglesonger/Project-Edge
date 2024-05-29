import pytest
from sqlalchemy.orm import Session
from backend.entities.user_entity import UserEntity
from backend.models.project import ProjectCreate, ProjectUpdate
from backend.entities.project_entity import ProjectEntity
from .reset_table_id_seq import reset_table_id_seq
from .user_data import user1, user2

# Project fixture
project = ProjectCreate(
    name="Test Project",
    description="A test project",
    current_users=[user1],
    owners=[user2]
)

new_project = ProjectCreate(
    name="Test Project",
    description="A test project",
    current_users=[user1],
    owners=[]
)

# Updated project data fixture
updated_project = ProjectUpdate(
    name="Updated Project",
    description="An updated description for the project",
    current_users=[user1, user2],
    owners=[user2]
)

updated_project_2 = ProjectUpdate(
    name="Updated Project 2",
    description="An updated 2 description for the project",
    current_users=[user1, user2],
    owners=[]
)

projects = [project]

def insert_fake_data(session: Session):
    user1_entity = session.query(UserEntity).filter_by(email=user1.email).first()
    user2_entity = session.query(UserEntity).filter_by(email=user2.email).first()

    entities = []
    for project in projects:
        entity = ProjectEntity(
            name=project.name,
            description=project.description,
            current_users=[user1_entity],
            owners=[user2_entity]
        )
        session.add(entity)
        entities.append(entity)
    session.commit()
    reset_table_id_seq(session, ProjectEntity, ProjectEntity.id, len(projects) + 1)

@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    insert_fake_data(session)
    yield
