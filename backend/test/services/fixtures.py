import pytest
from sqlalchemy.orm import Session

from backend.services.comment import CommentService
from backend.services.discussion import DiscussionService
from backend.services.project import ProjectService
from backend.services.user import UserService

from backend.test.services.demo_data import user_data, project_data, discussion_data, comment_data

@pytest.fixture()
def user_svc(session: Session):
    return UserService(session)

@pytest.fixture()
def add_test_user(user_svc: UserService):
    from .demo_data.user_data import user1
    user_svc.create_user(user1)
    yield

@pytest.fixture
def project_svc(session: Session) -> ProjectService:
    return ProjectService(session)

@pytest.fixture
def discussion_svc(session: Session) -> DiscussionService:
    return DiscussionService(session)

@pytest.fixture
def comment_svc(session: Session):
    return CommentService(session)

@pytest.fixture(autouse=True)
def setup_insert_data_fixture(session: Session):
    user_data.insert_fake_data(session)
    project_data.insert_fake_data(session)
    discussion_data.insert_fake_data(session)
    comment_data.insert_fake_data(session)
    session.commit()
    yield
