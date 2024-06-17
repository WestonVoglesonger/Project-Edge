import pytest
from sqlalchemy.orm import Session
from backend.entities.user_entity import UserEntity
from backend.models.project import ProjectCreate, ProjectUpdate
from backend.entities.project_entity import ProjectEntity
from ..reset_table_id_seq import reset_table_id_seq
from .user_data import user1, user2

# Project fixture
project = ProjectCreate(
    name="Test Project",
    description="A test project",
    team_members=[user1.to_user_response()],
    project_leaders=[user2.to_user_response()]
)

new_project = ProjectCreate(
    name="New Test Project",
    description="A new test project",
    team_members=[user1.to_user_response()],
    project_leaders=[]
)

# Updated project data fixture
updated_project = ProjectUpdate(
    name="Updated Project",
    description="An updated description for the project",
    team_members=[user1.to_user_response(), user2.to_user_response()],
    project_leaders=[user2.to_user_response()]
)

updated_project_2 = ProjectUpdate(
    name="Updated Project 2",
    description="An updated 2 description for the project",
    team_members=[user1.to_user_response(), user2.to_user_response()],
    project_leaders=[]
)

projects = [project]

def insert_fake_data(session: Session):
    user1_entity = session.query(UserEntity).filter_by(email=user1.email).first()
    user2_entity = session.query(UserEntity).filter_by(email=user2.email).first()

    if not user1_entity or not user2_entity:
        raise ValueError("User entities must be present in the database before inserting projects")

    entities = []
    for project in projects:
        team_members = [user1_entity] if user1_entity else []
        project_leaders = [user2_entity] if user2_entity else []
        entity = ProjectEntity.from_model(project, team_members, project_leaders)
        session.add(entity)
        entities.append(entity)
    session.commit()
    reset_table_id_seq(session, ProjectEntity, ProjectEntity.id, len(projects) + 1)

@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    insert_fake_data(session)
    yield
