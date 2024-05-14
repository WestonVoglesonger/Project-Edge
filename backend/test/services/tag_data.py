"""Mock data for users.

Three users are setup for testing and development purposes:

1. Rhonda Root (root user with all permissions)
2. Amy Ambassador (staff of XL with elevated permissions)
3. Sally Student (standard user without any special permissions)"""

import pytest
from sqlalchemy.orm import Session

from backend.entities.tag_entity import TagEntity
from backend.models.tag import Tag, TagBase
from .reset_table_id_seq import reset_table_id_seq

__authors__ = ["Weston Voglesonger"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


tag1 = Tag(
        id=1,
        name="AI"
    )

tag2 = Tag(
        id=2,
        name="Space"
    )

tag3 = Tag(
        id=3,
        name="Tech"
    )

new_tag = TagBase(
        name="Mathematics"
)

tags = [tag1, tag2, tag3]

def insert_fake_data(session: Session):
    global tags
    entities = []
    for tag in tags:
        entity = TagEntity.from_model(tag)
        session.add(entity)
        entities.append(entity)
    reset_table_id_seq(session, TagEntity, TagEntity.id, len(tags) + 1)
    session.commit()  # Commit to ensure Tag IDs in database

@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    insert_fake_data(session)
    session.commit()
    yield