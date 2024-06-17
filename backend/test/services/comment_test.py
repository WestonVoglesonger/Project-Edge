import pytest
from sqlalchemy.orm import Session

from backend.models.comment import CommentCreate, CommentUpdate
from backend.services.comment import CommentService
from backend.services.exceptions import CommentNotFoundException

# Data Setup and Injected Service Fixtures
from .demo_data.core_data import setup_insert_data_fixture
from .fixtures import comment_svc
from .demo_data.comment_data import new_comment_1, new_comment_2, comment, nested_comment, nested_comment_2


def test_create_comment(comment_svc: CommentService):
    created_comment = comment_svc.create_comment(new_comment_1)
    assert created_comment.description == new_comment_1.description
    assert created_comment.user_id == new_comment_1.user_id
    assert created_comment.discussion_id == new_comment_1.discussion_id


def test_create_nested_comment(comment_svc: CommentService):
    created_nested_comment = comment_svc.create_comment(nested_comment)
    assert created_nested_comment.description == nested_comment.description
    assert created_nested_comment.user_id == nested_comment.user_id
    assert created_nested_comment.parent_id == nested_comment.parent_id


def test_get_comments_by_project(comment_svc: CommentService):
    comments = comment_svc.get_comments_by_project(project_id=1)
    assert len(comments) == 1
    assert comments[0].description == comment.description
    assert comments[0].user_id == comment.user_id
    assert comments[0].project_id == comment.project_id


def test_get_comments_by_discussion(comment_svc: CommentService):
    comments = comment_svc.get_comments_by_discussion(discussion_id=1)
    assert len(comments) == 1
    assert comments[0].description == new_comment_2.description
    assert comments[0].user_id == new_comment_2.user_id
    assert comments[0].discussion_id == new_comment_2.discussion_id

def test_get_comments_by_parent(comment_svc: CommentService):
    comments = comment_svc.get_comments_by_parent(parent_id=1)
    assert len(comments) == 1
    assert comments[0].description == nested_comment_2.description
    assert comments[0].user_id == nested_comment_2.user_id
    assert comments[0].parent_id == nested_comment_2.parent_id

def test_update_comment(comment_svc: CommentService):
    created_comment = comment_svc.create_comment(new_comment_1)
    updated_comment_data = CommentUpdate(description="Updated Comment")
    updated_comment = comment_svc.update_comment(created_comment.id, updated_comment_data)
    assert updated_comment.description == updated_comment_data.description


def test_delete_comment(comment_svc: CommentService):
    comment_svc.delete_comment(1) # Ensure this matches the actual comment ID
    
    with pytest.raises(CommentNotFoundException):
        comment_svc.get_comment(1) # Ensure this matches the actual comment ID


def test_get_comment_not_found(comment_svc: CommentService):
    with pytest.raises(CommentNotFoundException):
        comment_svc.get_comment(999)


def test_update_comment_not_found(comment_svc: CommentService):
    with pytest.raises(CommentNotFoundException):
        comment_svc.update_comment(999, CommentUpdate(description="Updated Comment"))


def test_delete_comment_not_found(comment_svc: CommentService):
    with pytest.raises(CommentNotFoundException):
        comment_svc.delete_comment(999)
