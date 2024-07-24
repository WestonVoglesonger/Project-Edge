import pytest
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from backend.entities.user_entity import UserEntity
from backend.entities.project_entity import ProjectEntity
from backend.entities.join_request_entity import JoinRequestEntity
from backend.models.join_request import JoinRequestCreate, JoinRequestResponse
from ..reset_table_id_seq import reset_table_id_seq
from .user_data import user1, user2
from .project_data import project

# JoinRequest fixture
join_request_1 = JoinRequestCreate(
    user_id=1,
    project_id=1,

)

join_request_2 = JoinRequestCreate(
    user_id=2,
    project_id=1,
)

join_requests = [join_request_1, join_request_2]

def insert_fake_data(session: Session):
    user1_entity = session.query(UserEntity).filter_by(email=user1.email).first()
    user2_entity = session.query(UserEntity).filter_by(email=user2.email).first()
    project_entity = session.query(ProjectEntity).filter_by(name=project.name).first()

    if not user1_entity or not user2_entity or not project_entity:
        raise ValueError("User and Project entities must be present in the database before inserting join requests")

    entities = []
    for join_request in join_requests:
        join_request = JoinRequestEntity.from_model(join_request)
        join_request.user_id = user1_entity.id if join_request.user_id == 1 else user2_entity.id
        join_request.project_id = project_entity.id
        session.add(join_request)
        entities.append(join_request)
    session.commit()
    reset_table_id_seq(session, JoinRequestEntity, JoinRequestEntity.id, len(join_requests) + 1)

@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    insert_fake_data(session)
    yield
