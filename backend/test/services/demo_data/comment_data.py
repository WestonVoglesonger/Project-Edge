import pytest
from sqlalchemy.orm import Session
from backend.entities.comment_entity import CommentEntity
from backend.entities.discussion_entity import DiscussionEntity
from backend.entities.project_entity import ProjectEntity
from backend.entities.user_entity import UserEntity
from backend.models.comment import CommentCreate, CommentUpdate
from ..reset_table_id_seq import reset_table_id_seq
from .user_data import user1, user2
from .project_data import project
from .discussion_data import discussion


# Comment fixture
comment = CommentCreate(
    description="Test Comment",
    user_id=user1.id,
    project_id=1 # Ensure this matches the actual project ID
)

new_comment = CommentCreate(
    description="New Test Comment",
    user_id=user2.id,
    discussion_id=1 # Ensure this matches the actual discussion ID
)

# Updated comment data fixture
updated_comment = CommentUpdate(
    description="Updated Comment"
)

comments = [comment, new_comment]

def insert_fake_data(session: Session):
    user1_entity = session.query(UserEntity).filter_by(email=user1.email).first()
    user2_entity = session.query(UserEntity).filter_by(email=user2.email).first()
    project_entity = session.query(ProjectEntity).filter_by(name=project.name).first()
    discussion_entity = session.query(DiscussionEntity).filter_by(title=discussion.title).first()

    if not user1_entity or not user2_entity or not project_entity or not discussion_entity:
        raise ValueError("User, project, and discussion entities must be present in the database before inserting comments")

    entities = []
    for comment in comments:
        if comment.project_id:
            comment.project_id = project_entity.id
        if comment.discussion_id:
            comment.discussion_id = discussion_entity.id
        entity = CommentEntity.from_model(comment)
        session.add(entity)
        entities.append(entity)
    session.commit()
    reset_table_id_seq(session, CommentEntity, CommentEntity.id, len(comments) + 1)

@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    insert_fake_data(session)
    yield
