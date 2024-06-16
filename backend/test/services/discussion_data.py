import pytest
from sqlalchemy.orm import Session
from backend.entities.discussion_entity import DiscussionEntity
from backend.models.discussion import DiscussionCreate, DiscussionUpdate
from .reset_table_id_seq import reset_table_id_seq
from .user_data import user1, user2

# Discussion fixture
discussion = DiscussionCreate(
    title="Test Discussion",
    description="A test discussion",
    author_id=user1.id  # Ensure this matches the actual user ID
)

new_discussion = DiscussionCreate(
    title="New Discussion",
    description="A new test discussion",
    author_id=user2.id  # Ensure this matches the actual user ID
)

# Updated discussion data fixture
updated_discussion = DiscussionUpdate(
    title="Updated Discussion",
    description="An updated description for the discussion"
)

discussions = [discussion, new_discussion]

def insert_fake_data(session: Session):
    entities = []
    for discussion in discussions:
        entity = DiscussionEntity.from_model(discussion)
        session.add(entity)
        entities.append(entity)
    session.commit()
    reset_table_id_seq(session, DiscussionEntity, DiscussionEntity.id, len(discussions) + 1)

@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    insert_fake_data(session)
    yield
