"""Mock data for tags.

Tags are set up for testing and development purposes.

1. Tech
2. Science
3. Art
"""

import pytest
from sqlalchemy.orm import Session
from ...models.tag import Tag
from ...entities.tag_entity import TagEntity
from .reset_table_id_seq import reset_table_id_seq

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

tags = [
    Tag(name="Tech"),
    Tag(name="Science"),
    Tag(name="Art")
]

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
