import pytest
from sqlalchemy.orm import Session

from backend.entities.discussion_entity import DiscussionEntity
from backend.services.exceptions import (
    DiscussionNotFoundException,
    UserNotFoundException,
)
from backend.services.discussion import DiscussionService
from .discussion_data import updated_discussion
from .core_data import setup_insert_data_fixture
from .fixtures import discussion_svc, user_svc
from .discussion_data import discussion, new_discussion
from .user_data import user1, user2


def test_create_discussion(discussion_svc: DiscussionService):
    created_discussion = discussion_svc.create_discussion(discussion)
    assert created_discussion.title == discussion.title
    assert created_discussion.description == discussion.description
    assert created_discussion.author_id == discussion.author_id


def test_create_discussion_user_not_found(discussion_svc: DiscussionService):
    discussion.author_id = 999
    with pytest.raises(UserNotFoundException):
        discussion_svc.create_discussion(discussion)


def test_get_discussion(discussion_svc: DiscussionService):
    created_discussion = discussion_svc.create_discussion(discussion)
    fetched_discussion = discussion_svc.get_discussion(created_discussion.id)
    assert fetched_discussion.title == created_discussion.title
    assert fetched_discussion.description == created_discussion.description


def test_get_all_discussions(discussion_svc: DiscussionService):
    discussion_svc.create_discussion(new_discussion)

    # Fetch all discussions
    discussions = discussion_svc.get_all_discussions()

    # Assert that the correct number of discussions are fetched
    assert len(discussions) == 2


def test_update_discussion(discussion_svc: DiscussionService):
    created_discussion = discussion_svc.create_discussion(discussion)
    updated_discussion_data = discussion_svc.update_discussion(
        created_discussion.id, updated_discussion
    )
    assert updated_discussion_data.title == updated_discussion.title
    assert updated_discussion_data.description == updated_discussion.description


def test_delete_discussion(discussion_svc: DiscussionService):
    created_discussion = discussion_svc.create_discussion(discussion)
    discussion_svc.delete_discussion(created_discussion.id)

    with pytest.raises(DiscussionNotFoundException):
        discussion_svc.get_discussion(created_discussion.id)


def test_get_discussion_not_found(discussion_svc: DiscussionService):
    with pytest.raises(DiscussionNotFoundException):
        discussion_svc.get_discussion(999)


def test_update_discussion_not_found(discussion_svc: DiscussionService):
    with pytest.raises(DiscussionNotFoundException):
        discussion_svc.update_discussion(999, updated_discussion)


def test_delete_discussion_not_found(discussion_svc: DiscussionService):
    with pytest.raises(DiscussionNotFoundException):
        discussion_svc.delete_discussion(999)
