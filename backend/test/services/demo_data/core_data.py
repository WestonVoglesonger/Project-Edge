"""Helper data file that is used commonly for users, roles, and permissions.

Rather than importing each of these data insertion fixtures directly into tests,
this module serves as a helper to bring them all in at once.
"""

import pytest
from sqlalchemy.orm import Session

from backend.test.services.demo_data import project_data
from backend.test.services.demo_data import discussion_data
from backend.test.services.demo_data import comment_data
from . import user_data

__authors__ = ["Weston Voglesonger"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

@pytest.fixture(autouse=True)
def setup_insert_data_fixture(session: Session):
    user_data.insert_fake_data(session)
    project_data.insert_fake_data(session)
    discussion_data.insert_fake_data(session)
    comment_data.insert_fake_data(session)
    session.commit()
    yield
