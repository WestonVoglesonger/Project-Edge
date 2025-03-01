"""SQLAlchemy DB Engine and Session niceties for FastAPI dependency injection."""

import sqlalchemy
from sqlalchemy.orm import Session
from .env import getenv

__authors__ = ["Weston Voglesonger"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


def _engine_str(database: str = getenv("POSTGRES_DATABASE")) -> str:
    """Helper function for reading settings from environment variables to produce connection string."""
    dialect = "postgresql+psycopg2"
    user = getenv("POSTGRES_USER")
    password = getenv("POSTGRES_PASSWORD")
    host = getenv("POSTGRES_HOST")
    port = getenv("POSTGRES_PORT")

    # Add SSL mode parameter if we're in production mode (for services like Render)
    if getenv("MODE") == "production":
        return f"{dialect}://{user}:{password}@{host}:{port}/{database}?sslmode=require"

    return f"{dialect}://{user}:{password}@{host}:{port}/{database}"


# Create the SQLAlchemy engine with appropriate settings
mode = getenv("MODE") or "development"
engine_settings = {}

# For production, use less verbose logging and handle reconnections better
if mode == "production":
    engine_settings = {
        "echo": False,
        "pool_size": 5,
        "max_overflow": 10,
        "pool_recycle": 300,  # Recycle connections every 5 minutes
        "pool_pre_ping": True,  # Verify connection is still alive
    }
else:
    engine_settings = {"echo": True}  # Keep echo for development

engine = sqlalchemy.create_engine(_engine_str(), **engine_settings)
"""Application-level SQLAlchemy database engine."""


def db_session():
    """Generator function offering dependency injection of SQLAlchemy Sessions."""
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
