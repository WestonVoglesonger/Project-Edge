"""Fixtures used for testing the core services."""

import pytest
from sqlalchemy.orm import Session

from backend.services.user import UserService

__authors__ = ["Weston Voglesonger"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


@pytest.fixture()
def user_svc(session: Session):
    """This fixture is used to test the UserService class."""
    return UserService(session)

@pytest.fixture()
def add_test_user(user_svc: UserService):
    """This fixture adds a test user to the database."""
    from .user_data import user
    user_svc.create_user(user)
    yield