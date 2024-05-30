import pytest
from sqlalchemy.orm import Session

from backend.services.exceptions import ProjectNotFoundException
from backend.services.project import ProjectService
from backend.services.user import UserService
from .project_data import updated_project
from backend.services.exceptions import UserNotFoundException


# Data Setup and Injected Service Fixtures
from .core_data import setup_insert_data_fixture
from .fixtures import project_svc, user_svc
from .project_data import project, new_project, updated_project_2
from .user_data import user1, user2

def test_create_project(project_svc: ProjectService):
    created_project = project_svc.create_project(project)
    assert created_project.name == project.name
    assert created_project.description == project.description
    assert created_project.current_users[0].email == project.current_users[0].email
    assert created_project.owners[0].email == project.owners[0].email

def test_create_project_no_owners(project_svc: ProjectService):
    created_project = project_svc.create_project(new_project)
    assert created_project.owners == new_project.owners

def test_get_project(project_svc: ProjectService):
    created_project = project_svc.create_project(project)
    fetched_project = project_svc.get_project(created_project.id)
    assert fetched_project.name == created_project.name
    assert fetched_project.description == created_project.description

def test_get_all_projects(project_svc: ProjectService):
    project_svc.create_project(new_project)

    # Fetch all projects
    projects = project_svc.get_all_projects()

    # Assert that the correct number of projects are fetched
    assert len(projects) == 2

def test_update_project(project_svc: ProjectService):
    created_project = project_svc.create_project(project)
    updated_project_data = project_svc.update_project(created_project.id, updated_project)
    assert updated_project_data.name == updated_project.name
    assert updated_project_data.description == updated_project.description

def test_update_project_remove_owners(project_svc: ProjectService):
    created_project = project_svc.create_project(project)
    updated_project_data = project_svc.update_project(created_project.id, updated_project_2)
    assert updated_project_data.owners == updated_project_2.owners

def test_delete_project(project_svc: ProjectService):    
    created_project = project_svc.create_project(project)
    project_svc.delete_project(created_project.id)
    
    with pytest.raises(ProjectNotFoundException):
        project_svc.get_project(created_project.id)

def test_get_project_not_found(project_svc: ProjectService):
    with pytest.raises(ProjectNotFoundException):
        project_svc.get_project(999)

def test_update_project_not_found(project_svc: ProjectService):
    with pytest.raises(ProjectNotFoundException):
        project_svc.update_project(999, updated_project)
    
def test_delete_project_not_found(project_svc: ProjectService):
    with pytest.raises(ProjectNotFoundException):
        project_svc.delete_project(999)

def test_search_users_by_partial_name(user_svc: UserService):
    users = user_svc.search_users_by_name("Sal")
    assert len(users) == 1
    assert users[0].first_name == user1.first_name
    assert users[0].email == user1.email

def test_search_users_by_full_name(user_svc: UserService):
    users = user_svc.search_users_by_name("Sally Doe")
    assert len(users) == 1
    assert users[0].first_name == user1.first_name
    assert users[0].last_name == user1.last_name
    assert users[0].email == user1.email

def test_search_users_by_last_name(user_svc: UserService):
    users = user_svc.search_users_by_name("Doe")
    assert len(users) == 2
    assert users[0].last_name == user2.last_name
    assert users[0].email == user1.email

def test_search_users_multiple_matches(user_svc: UserService):
    users = user_svc.search_users_by_name("doe")
    assert len(users) == 2
    assert any(user.email == user1.email for user in users)
    assert any(user.email == user2.email for user in users)
