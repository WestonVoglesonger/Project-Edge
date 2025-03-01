"""SQLAlchemy DB Engine and Session niceties for FastAPI dependency injection."""

import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.pool import NullPool
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
    mode = getenv("MODE") or "development"
    if mode == "production":
        # Enhanced SSL configuration for Render PostgreSQL
        return f"{dialect}://{user}:{password}@{host}:{port}/{database}?sslmode=require&connect_timeout=10"

    return f"{dialect}://{user}:{password}@{host}:{port}/{database}"


# Create the SQLAlchemy engine with appropriate settings
mode = getenv("MODE") or "development"
engine_settings = {}

if mode == "production":
    engine_settings = {
        "echo": False,
        "poolclass": NullPool,  # Disable connection pooling
        "connect_args": {
            "connect_timeout": 10,  # Connection timeout of 10 seconds
            "keepalives": 1,  # Enable keepalives
            "keepalives_idle": 60,  # Idle time before sending keepalive
            "keepalives_interval": 10,  # Interval between keepalives
            "keepalives_count": 3,  # Number of keepalives before dropping
            "sslmode": "require",
        },
    }
else:
    engine_settings = {"echo": True}  # Keep echo for development

engine = sqlalchemy.create_engine(_engine_str(), **engine_settings, echo_pool="debug")
"""Application-level SQLAlchemy database engine."""


def db_session():
    """Generator function offering dependency injection of SQLAlchemy Sessions."""
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
