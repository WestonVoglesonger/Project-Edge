import pytest
from sqlalchemy.orm import Session

from backend.models.comment import CommentCreate, CommentUpdate
from backend.services.comment import CommentService
from backend.services.exceptions import CommentNotFoundException

# Data Setup and Injected Service Fixtures
from .demo_data.core_data import setup_insert_data_fixture
from .fixtures import comment_svc
from .demo_data.comment_data import new_comment, comment, updated_comment


def test_create_comment(comment_svc: CommentService):
    created_comment = comment_svc.create_comment(new_comment)
    assert created_comment.description == new_comment.description
    assert created_comment.user_id == new_comment.user_id
    assert created_comment.discussion_id == new_comment.discussion_id


def test_get_comments_by_post(comment_svc: CommentService):
    comments = comment_svc.get_comments_by_project(project_id=1)
    assert len(comments) == 1
    assert comments[0].description == comment.description
    assert comments[0].user_id == comment.user_id
    assert comments[0].project_id == comment.project_id


def test_update_comment(comment_svc: CommentService):
    created_comment = comment_svc.create_comment(new_comment)
    updated_comment_data = CommentUpdate(description="Updated Comment")
    updated_comment = comment_svc.update_comment(created_comment.id, updated_comment_data)
    assert updated_comment.description == updated_comment_data.description


def test_delete_comment(comment_svc: CommentService):
    created_comment = comment_svc.create_comment(new_comment)
    comment_svc.delete_comment(created_comment.id)
    
    with pytest.raises(CommentNotFoundException):
        comment_svc.get_comment(created_comment.id)


def test_get_comment_not_found(comment_svc: CommentService):
    with pytest.raises(CommentNotFoundException):
        comment_svc.get_comment(999)


def test_update_comment_not_found(comment_svc: CommentService):
    with pytest.raises(CommentNotFoundException):
        comment_svc.update_comment(999, CommentUpdate(description="Updated Comment"))


def test_delete_comment_not_found(comment_svc: CommentService):
    with pytest.raises(CommentNotFoundException):
        comment_svc.delete_comment(999)
