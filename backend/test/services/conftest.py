import pytest
from sqlalchemy import create_engine, text, Engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError, ProgrammingError

from backend.entities.base import Base
from ...database import _engine_str
from ...env import getenv

POSTGRES_DATABASE = f'{getenv("POSTGRES_DATABASE")}_test'
POSTGRES_USER = getenv("POSTGRES_USER")

def reset_database():
    engine = create_engine(_engine_str(""))
    with engine.connect() as connection:
        try:
            conn = connection.execution_options(autocommit=False)
            conn.execute(text("ROLLBACK"))  # Get out of transactional mode...
            conn.execute(text(f"DROP DATABASE {POSTGRES_DATABASE}"))
        except ProgrammingError:
            pass
        except OperationalError:
            print("Could not drop database because it's being accessed by others (psql open?)")
            exit(1)

        conn.execute(text(f"CREATE DATABASE {POSTGRES_DATABASE}"))
        conn.execute(
            text(f"GRANT ALL PRIVILEGES ON DATABASE {POSTGRES_DATABASE} TO {POSTGRES_USER}")
        )

@pytest.fixture(scope="session")
def test_engine() -> Engine:
    reset_database()
    return create_engine(_engine_str(POSTGRES_DATABASE))

@pytest.fixture(scope="function")
def session(test_engine: Engine):
    Base.metadata.drop_all(test_engine)
    Base.metadata.create_all(test_engine)
    session = Session(test_engine)
    try:
        yield session
    finally:
        session.close()
