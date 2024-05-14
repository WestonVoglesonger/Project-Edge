import pytest
from backend.models.tag import TagBase
from backend.services.tag import TagService
from backend.exceptions import TagNotFoundException

# Data Setup and Injected Service Fixtures
from .core_data import setup_insert_data_fixture
from .fixtures import  tag_svc

from .tag_data import new_tag, tag1, tag2, tag3


def test_create_tag(tag_svc: TagService):
    created_tag = tag_svc.create_tag(new_tag)

    assert created_tag.name == new_tag.name
    assert created_tag.id is not None

def test_get_tag(tag_svc: TagService):
    fetched_tag = tag_svc.get_tag(tag1.id)
    assert fetched_tag.id == tag1.id
    assert fetched_tag.name == tag1.name

def test_get_tag_not_found(tag_svc: TagService):
    with pytest.raises(TagNotFoundException):
        tag_svc.get_tag(tag_id=999)

def test_delete_tag(tag_svc: TagService):
    tag_data = TagBase(name="Art")
    created_tag = tag_svc.create_tag(tag_data)
    tag_svc.delete_tag(created_tag.id)
    with pytest.raises(TagNotFoundException):
        tag_svc.get_tag(created_tag.id)
