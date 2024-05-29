import pytest
from sqlalchemy.orm import Session

from backend.services.exceptions import ProjectNotFoundException
from backend.services.project import ProjectService
from .project_data import updated_project

# Data Setup and Injected Service Fixtures
from .core_data import setup_insert_data_fixture
from .fixtures import project_svc
from .project_data import project, new_project, updated_project_2

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
