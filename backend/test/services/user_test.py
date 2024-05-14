import pytest
from sqlalchemy.orm import Session

from backend.exceptions import EmailAlreadyRegisteredException, UserNotFoundException
from backend.models.user import ProfileForm, UserBase
from backend.services.user import UserService

# Data Setup and Injected Service Fixtures
from .core_data import setup_insert_data_fixture
from .fixtures import  user_svc

from .user_data import new_user, user, project_owner, root, update_data



def test_create_user(user_svc: UserService):
    created_user = user_svc.create_user(new_user)
    assert created_user.email == new_user.email
    assert created_user.accepted_community_agreement == new_user.accepted_community_agreement

def test_get_user(user_svc: UserService):
    created_user = user_svc.create_user(new_user)
    fetched_user = user_svc.get_user(created_user.id)
    assert fetched_user.email == created_user.email
    assert created_user.accepted_community_agreement == new_user.accepted_community_agreement

def test_update_user(user_svc: UserService):
    updated_user = user_svc.update_user(user.id, update_data)
    assert updated_user.email == update_data.email
    assert updated_user.first_name == update_data.first_name
    assert updated_user.last_name == update_data.last_name

def test_delete_user(user_svc: UserService):    
    user_svc.delete_user(user.id)
    
    with pytest.raises(UserNotFoundException):
        user_svc.get_user(user.id)

def test_create_user_with_existing_email(user_svc: UserService):    
    with pytest.raises(EmailAlreadyRegisteredException):
        user_svc.create_user(user)

def test_get_user_not_found(user_svc: UserService):
    with pytest.raises(UserNotFoundException):
        user_svc.get_user(999)

def test_update_user_not_found(user_svc: UserService):
    with pytest.raises(UserNotFoundException):
        user_svc.update_user(999, update_data)
    
def test_delete_user_not_found(user_svc: UserService):
    with pytest.raises(UserNotFoundException):
        user_svc.delete_user(999)
