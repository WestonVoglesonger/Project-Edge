import pytest
from backend.models.join_request import JoinRequestCreate
from backend.services.exceptions import JoinRequestAlreadyMadeException, UserNotFoundException, ProjectNotFoundException, JoinRequestNotFoundException
from backend.services.join_request import JoinRequestService

# Data Setup and Injected Service Fixtures
from .demo_data.core_data import setup_insert_data_fixture
from .fixtures import join_request_svc
from .demo_data.join_request_data import join_request_1, join_request_2


def test_create_join_request(join_request_svc: JoinRequestService):
    join_request = join_request_svc.create_join_request(join_request_2)
    assert join_request.user_id == join_request_2.user_id
    assert join_request.project_id == join_request_2.project_id

def test_create_join_request_user_not_found(join_request_svc: JoinRequestService):
    join_request_data = JoinRequestCreate(user_id=999, project_id=1)
    with pytest.raises(UserNotFoundException):
        join_request_svc.create_join_request(join_request_data)

def test_create_join_request_project_not_found(join_request_svc: JoinRequestService):
    join_request_data = JoinRequestCreate(user_id=1, project_id=999)
    with pytest.raises(ProjectNotFoundException):
        join_request_svc.create_join_request(join_request_data)

def test_create_join_request_exists(join_request_svc: JoinRequestService):
    join_request_svc.create_join_request(join_request_1)
    with pytest.raises(JoinRequestAlreadyMadeException):
        join_request_svc.create_join_request(join_request_1)
    
def test_get_join_request(join_request_svc: JoinRequestService):
    join_request = join_request_svc.create_join_request(join_request_1)
    retrieved_join_request = join_request_svc.get_join_request(join_request.id)
    assert retrieved_join_request.id == join_request.id

def test_get_join_request_not_found(join_request_svc: JoinRequestService):
    with pytest.raises(JoinRequestNotFoundException):
        join_request_svc.get_join_request(999)

def test_list_join_requests(join_request_svc: JoinRequestService):
    join_request_svc.create_join_request(join_request_1)
    join_request_svc.create_join_request(join_request_2)
    join_requests = join_request_svc.list_join_requests()
    assert len(join_requests) == 2

def test_delete_join_request(join_request_svc: JoinRequestService):
    join_request = join_request_svc.create_join_request(join_request_1)
    join_request_svc.delete_join_request(join_request.user_id, join_request.project_id)
    with pytest.raises(JoinRequestNotFoundException):
        join_request_svc.get_join_request(join_request.id)

def test_delete_join_request_not_found(join_request_svc: JoinRequestService):
    with pytest.raises(JoinRequestNotFoundException):
        join_request_svc.delete_join_request(999, 999)
