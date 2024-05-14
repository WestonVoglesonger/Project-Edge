import pytest
from sqlalchemy.orm import Session
from backend.models.tag import TagBase
from backend.services.tag import TagService

def test_create_tag(session: Session):
    tag_service = TagService(session)
    
    tag_data = TagBase(name="testtag")
    
    created_tag = tag_service.create_tag(tag_data)
    assert created_tag.name == tag_data.name

def test_get_tag(session: Session):
    tag_service = TagService(session)
    
    tag_data = TagBase(name="testtag")
    
    created_tag = tag_service.create_tag(tag_data)
    fetched_tag = tag_service.get_tag(created_tag.id)
    assert fetched_tag.name == created_tag.name

def test_get_tags(session: Session):
    tag_service = TagService(session)
    
    tag_data1 = TagBase(name="testtag1")
    tag_data2 = TagBase(name="testtag2")
    
    tag_service.create_tag(tag_data1)
    tag_service.create_tag(tag_data2)
    
    tags = tag_service.get_tags()
    assert len(tags) == 2

def test_update_tag(session: Session):
    tag_service = TagService(session)
    
    tag_data = TagBase(name="testtag")
    
    created_tag = tag_service.create_tag(tag_data)
    
    update_data = TagBase(name="updatedtag")
    updated_tag = tag_service.update_tag(created_tag.id, update_data)
    assert updated_tag.name == update_data.name

def test_delete_tag(session: Session):
    tag_service = TagService(session)
    
    tag_data = TagBase(name="testtag")
    
    created_tag = tag_service.create_tag(tag_data)
    
    tag_service.delete_tag(created_tag.id)
    
    with pytest.raises(ValueError):
        tag_service.get_tag(created_tag.id)
