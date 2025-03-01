"""SQLAlchemy DB Engine and Session niceties for FastAPI dependency injection."""

import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.pool import NullPool
from sqlalchemy import event
from sqlalchemy.exc import OperationalError, DBAPIError
import logging
import time
from typing import Optional
from .env import getenv

__authors__ = ["Weston Voglesonger"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

logger = logging.getLogger(__name__)


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
        return f"{dialect}://{user}:{password}@{host}:{port}/{database}?sslmode=require"

    return f"{dialect}://{user}:{password}@{host}:{port}/{database}"


# Create the SQLAlchemy engine with appropriate settings
mode = getenv("MODE") or "development"
engine_settings = {}

if mode == "production":
    engine_settings = {
        "echo": False,
        "poolclass": NullPool,  # Stick with NullPool as requested
        "pool_pre_ping": True,  # Check connection validity before using it
        "pool_recycle": 180,  # Recycle connections after 3 minutes
        "connect_args": {
            "connect_timeout": 10,  # Connection timeout of 10 seconds
            "application_name": "project-edge-app",  # Identify app in pg_stat_activity
            "keepalives": 1,  # Enable keepalives
            "keepalives_idle": 30,  # Shorter idle time (30 sec) before sending keepalive
            "keepalives_interval": 10,  # Interval between keepalives
            "keepalives_count": 5,  # More keepalives before dropping
        },
    }
else:
    engine_settings = {"echo": True}  # Keep echo for development


# Create engine with retry capability
max_retries = 3 if mode == "production" else 0
retry_interval = 3  # seconds


def create_engine_with_retry():
    """Create engine with retry logic for handling temporary connection issues."""
    attempt = 0
    last_error = None

    while attempt <= max_retries:
        try:
            if attempt > 0:
                logger.warning(
                    f"Retrying database connection, attempt {attempt} of {max_retries}"
                )

            eng = sqlalchemy.create_engine(_engine_str(), **engine_settings)

            # Test connection
            if mode == "production":
                with eng.connect() as conn:
                    conn.execute(sqlalchemy.text("SELECT 1"))
                logger.info("Database connection successfully established")

            return eng

        except (OperationalError, DBAPIError) as e:
            last_error = e
            logger.warning(f"Database connection failed: {e}")
            if attempt < max_retries:
                time.sleep(retry_interval)
            attempt += 1

    logger.error(
        f"Failed to connect to database after {max_retries} attempts: {last_error}"
    )
    # Return the engine anyway, will fail later but at least the app will start
    return sqlalchemy.create_engine(_engine_str(), **engine_settings)


engine = create_engine_with_retry()
"""Application-level SQLAlchemy database engine."""


# For production, add connection event listeners to better handle disconnects
if mode == "production":

    @event.listens_for(engine, "connect")
    def connect(dbapi_connection: object, connection_record: object) -> None:
        logger.debug("New database connection established")

    @event.listens_for(engine, "checkout")
    def checkout(
        dbapi_connection: object, connection_record: object, connection_proxy: object
    ) -> None:
        logger.debug("Database connection checkout")

    @event.listens_for(engine, "invalidate")
    def invalidate(
        dbapi_connection: object, connection_record: object, exception: Exception
    ) -> None:
        logger.warning(f"Database connection invalidated due to: {exception}")


def db_session():
    """Generator function offering dependency injection of SQLAlchemy Sessions with retry capability."""
    retry_count = 0
    max_session_retries = 3 if mode == "production" else 0

    while True:
        try:
            session = Session(engine)
            try:
                # Test session if in production
                if mode == "production":
                    session.execute(sqlalchemy.text("SELECT 1"))

                yield session
                break
            finally:
                session.close()

        except (OperationalError, DBAPIError) as e:
            retry_count += 1
            if retry_count <= max_session_retries:
                logger.warning(
                    f"Session creation failed, retrying ({retry_count}/{max_session_retries}): {e}"
                )
                time.sleep(1)
            else:
                logger.error(
                    f"Failed to create database session after {max_session_retries} attempts: {e}"
                )
                raise
