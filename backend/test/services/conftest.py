from os import getenv
from typing import Generator
import pytest
from sqlalchemy import create_engine, text, Engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError, ProgrammingError

from backend.database import _engine_str
from backend.entities.user_entity import Base

POSTGRES_DATABASE = f'{getenv("POSTGRES_DATABASE")}_test'
POSTGRES_USER = getenv("POSTGRES_USER")

def reset_database():
    engine = create_engine(_engine_str(""))
    with engine.connect() as connection:
        try:
            conn = connection.execution_options(autocommit=False)
            conn.execute(text("ROLLBACK"))
            conn.execute(text(f"DROP DATABASE IF EXISTS {POSTGRES_DATABASE}"))
        except (ProgrammingError, OperationalError):
            ...
        conn.execute(text(f"CREATE DATABASE {POSTGRES_DATABASE}"))
        conn.execute(
            text(f"GRANT ALL PRIVILEGES ON DATABASE {POSTGRES_DATABASE} TO {POSTGRES_USER}")
        )

@pytest.fixture(scope="session")
def test_engine() -> Engine:
    reset_database()
    return create_engine(_engine_str(POSTGRES_DATABASE))

@pytest.fixture(scope="function")
def session(test_engine: Engine) -> Generator[Session, None, None]:
    Base.metadata.create_all(test_engine) 
    session = Session(test_engine)
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(test_engine) 