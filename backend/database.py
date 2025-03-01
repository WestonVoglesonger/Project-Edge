"""SQLAlchemy DB Engine and Session niceties for FastAPI dependency injection."""

import os
import time
import logging
import sqlalchemy
from sqlalchemy.orm import Session, scoped_session, sessionmaker
from sqlalchemy.exc import OperationalError, DBAPIError
from .env import getenv

__authors__ = ["Weston Voglesonger"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

logger = logging.getLogger(__name__)

# Get environment variables
mode = getenv("MODE") or "development"


# Simplified direct connection string approach
def get_database_url():
    """Get the database URL from environment or construct it."""
    # Check if Render provides a DATABASE_URL (they often do for managed databases)
    render_db_url = os.environ.get("DATABASE_URL")
    if render_db_url and mode == "production":
        # Use the provided URL directly
        logger.info("Using Render-provided DATABASE_URL")
        return render_db_url

    # Construct our own if not provided
    user = getenv("POSTGRES_USER")
    password = getenv("POSTGRES_PASSWORD")
    host = getenv("POSTGRES_HOST")
    port = getenv("POSTGRES_PORT")
    database = getenv("POSTGRES_DATABASE")

    if mode == "production":
        # Force SSL for production - very simple approach
        return (
            f"postgresql://{user}:{password}@{host}:{port}/{database}?sslmode=require"
        )
    else:
        return f"postgresql://{user}:{password}@{host}:{port}/{database}"


# Create engine with minimal settings to avoid complexity
def create_db_engine():
    """Create a database engine with minimal configuration and retry logic."""
    url = get_database_url()
    logger.info(f"Connecting to database in {mode} mode")

    # Keep configuration extremely minimal for production
    if mode == "production":
        return sqlalchemy.create_engine(
            url,
            pool_pre_ping=True,  # Essential health check
            pool_size=1,  # Minimal connections to reduce SSL issues
            max_overflow=2,  # Allow only 2 overflow connections
            pool_recycle=300,  # Recycle connections every 5 minutes
        )
    else:
        # Development configuration
        return sqlalchemy.create_engine(url, echo=True)


# Create engine with retry logic
engine = None
for attempt in range(5):  # Try 5 times at startup
    try:
        if attempt > 0:
            logger.warning(f"Retrying database connection, attempt {attempt+1} of 5")
            time.sleep(3)  # Wait between attempts

        engine = create_db_engine()

        # Test connection minimally
        if mode == "production":
            with engine.connect() as conn:
                conn.execute(sqlalchemy.text("SELECT 1"))
                logger.info("✅ Initial database connection successful")
        break
    except Exception as e:
        logger.warning(f"Database connection attempt {attempt+1} failed: {e}")
        if attempt == 4:  # Last attempt
            logger.error(
                f"❌ All database connection attempts failed, but continuing app startup"
            )
            # Create engine anyway - will retry later
            engine = create_db_engine()

# Create session factory
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def db_session():
    """Generator function offering dependency injection of SQLAlchemy Sessions with retry capability."""
    session = None

    # Try up to 3 times for each request
    for attempt in range(3):
        try:
            if attempt > 0:
                logger.warning(f"Retrying to create session, attempt {attempt+1}/3")
                time.sleep(1)

            session = SessionFactory()

            # Verify connection with minimal query if in production
            if mode == "production" and attempt == 0:  # Only on first attempt
                session.execute(sqlalchemy.text("SELECT 1"))

            break  # Connection successful, break the retry loop

        except Exception as e:
            if session:
                session.close()
                session = None  # Reset session after closing

            if attempt == 2:  # Last attempt
                logger.error(f"Failed to create database session after 3 attempts: {e}")
                raise

    # If we have a session, yield it and ensure it's closed after use
    if session:
        try:
            yield session
        except Exception as e:
            # Log any exceptions that occur while the session is being used
            logger.error(f"Exception occurred during session usage: {e}")
            raise  # Re-raise the exception after logging
        finally:
            # Always close the session, even if an exception occurred
            session.close()
    else:
        # This should never happen because we should have raised an exception in the retry loop
        # But just in case...
        logger.error("Failed to create database session but did not raise an exception")
        raise Exception("Could not create database session")
