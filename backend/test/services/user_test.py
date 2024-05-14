import pytest
from sqlalchemy.orm import Session

from backend.exceptions import EmailAlreadyRegisteredException, UserNotFoundException
from backend.models.user import ProfileForm, UserBase
from backend.services.user import UserService

def test_create_user(session: Session):
    user_service = UserService(session)
    
    user_data = UserBase(
        first_name="Test",
        last_name="User",
        email="testuser@example.com",
        password="testpassword",
        accepted_community_agreement=True
    )
    
    created_user = user_service.create_user(user_data)
    assert created_user.email == user_data.email
    assert created_user.first_name == user_data.first_name
    assert created_user.last_name == user_data.last_name

def test_get_user(session: Session):
    user_service = UserService(session)
    
    user_data = UserBase(
        first_name="Test",
        last_name="User",
        email="testuser@example.com",
        password="testpassword",
        accepted_community_agreement=True
    )
    
    created_user = user_service.create_user(user_data)
    fetched_user = user_service.get_user(created_user.id)
    assert fetched_user.email == created_user.email
    assert fetched_user.first_name == created_user.first_name
    assert fetched_user.last_name == created_user.last_name

def test_update_user(session: Session):
    user_service = UserService(session)
    
    user_data = UserBase(
        first_name="Test",
        last_name="User",
        email="testuser@example.com",
        password="testpassword",
        accepted_community_agreement=True
    )
    
    created_user = user_service.create_user(user_data)
    
    update_data = ProfileForm(
        first_name="Updated",
        last_name="User",
        email="updateduser@example.com",
        password="updatedpassword",
        accepted_community_agreement=True
    )
    
    updated_user = user_service.update_user(created_user.id, update_data)
    assert updated_user.email == update_data.email
    assert updated_user.first_name == update_data.first_name
    assert updated_user.last_name == update_data.last_name

def test_delete_user(session: Session):
    user_service = UserService(session)
    
    user_data = UserBase(
        first_name="Test",
        last_name="User",
        email="testuser@example.com",
        password="testpassword",
        accepted_community_agreement=True
    )
    
    created_user = user_service.create_user(user_data)
    
    user_service.delete_user(created_user.id)
    
    with pytest.raises(UserNotFoundException):
        user_service.get_user(created_user.id)

def test_create_user_with_existing_email(session: Session):
    user_service = UserService(session)
    
    user_data = UserBase(
        first_name="Test",
        last_name="User",
        email="testuser@example.com",
        password="testpassword",
        accepted_community_agreement=True
    )
    
    user_service.create_user(user_data)
    
    with pytest.raises(EmailAlreadyRegisteredException):
        user_service.create_user(user_data)

def test_get_user_not_found(session: Session):
    user_service = UserService(session)
    
    with pytest.raises(UserNotFoundException):
        user_service.get_user(999)

def test_update_user_not_found(session: Session):
    user_service = UserService(session)
    
    update_data = ProfileForm(
        first_name="Updated",
        last_name="User",
        email="updateduser@example.com",
        password="updatedpassword",
        accepted_community_agreement=True
    )
    
    with pytest.raises(UserNotFoundException):
        user_service.update_user(999, update_data)
    
def test_delete_user_not_found(session: Session):
    user_service = UserService(session)
    
    with pytest.raises(UserNotFoundException):
        user_service.delete_user(999)
