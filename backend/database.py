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

def _engine_str(database: str = getenv("POSTGRES_DATABASE")) -> str:
    """Helper function for reading settings from environment variables to produce connection string."""
    dialect = "postgresql+psycopg2"
    user = getenv("POSTGRES_USER")
    password = getenv("POSTGRES_PASSWORD")
    host = getenv("POSTGRES_HOST")
    port = getenv("POSTGRES_PORT")
    return f"{dialect}://{user}:{password}@{host}:{port}/{database}"

# Simplified direct connection string approach
def get_database_url():
    """Get the database URL from environment or construct it."""

    # Debug: Print all environment variables to help diagnose the issue
    if mode == "production":
        logger.info("Environment variables:")
        for key, value in os.environ.items():
            # Mask sensitive values
            if "PASSWORD" in key or "SECRET" in key:
                logger.info(f"{key}=***MASKED***")
            else:
                logger.info(f"{key}={value}")

    # Check if Render provides a DATABASE_URL (they often do for managed databases)
    render_db_url = os.environ.get("DATABASE_URL")
    internal_db_url = os.environ.get("RENDER_DATABASE_URL")

    if render_db_url and mode == "production":
        # Use the provided URL directly
        logger.info(f"Using Render-provided DATABASE_URL: {render_db_url[:20]}...")
        return render_db_url
    elif internal_db_url and mode == "production":
        # Use the internal URL provided by Render
        logger.info(
            f"Using Render-provided RENDER_DATABASE_URL: {internal_db_url[:20]}..."
        )
        return internal_db_url

    # Construct our own if not provided
    user = getenv("POSTGRES_USER")
    password = getenv("POSTGRES_PASSWORD")
    host = getenv("POSTGRES_HOST")
    port = getenv("POSTGRES_PORT")
    database = getenv("POSTGRES_DATABASE")

    # Log the host we're attempting to connect to
    logger.info(f"Using constructed connection string with host: {host}")

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
        # Try to create with the most minimal settings possible for Render
        # This is specifically to avoid SSL issues
        engine_settings = {
            "pool_pre_ping": True,
            "pool_size": 1,
            "max_overflow": 2,
            "pool_recycle": 300,
            "connect_args": {
                # Trying different SSL settings to avoid SSL connection issues
                "sslmode": "require",
                "connect_timeout": 10,  # Shorter timeout
                # Add application_name to help identify connections in logs
                "application_name": "project-edge-web",
            },
        }

        # Log the final URL (without password) and settings for debugging
        safe_url = url.replace(url.split("@")[0], "postgresql://****:****")
        logger.info(f"Creating engine with URL: {safe_url}")
        logger.info(f"Engine settings: {engine_settings}")

        return sqlalchemy.create_engine(url, **engine_settings)
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
                logger.info("Successfully executed test query in session")

            break  # Connection successful, break the retry loop

        except sqlalchemy.exc.OperationalError as e:
            if session:
                session.close()
                session = None  # Reset session after closing

            # Extract the root cause for better debugging
            root_cause = str(e.orig) if hasattr(e, "orig") else str(e)
            logger.error(
                f"Database connection error (attempt {attempt+1}/3): {root_cause}"
            )

            # Log more details about SSL errors
            if "SSL" in root_cause:
                logger.error(
                    "SSL connection issue detected. This may be due to network issues or certificate problems."
                )

            if attempt == 2:  # Last attempt
                logger.error(f"Failed to create database session after 3 attempts: {e}")
                raise

        except Exception as e:
            if session:
                session.close()
                session = None  # Reset session after closing

            logger.error(
                f"Unexpected error during session creation (attempt {attempt+1}/3): {str(e)}"
            )
            if attempt == 2:  # Last attempt
                logger.error(f"Failed to create database session after 3 attempts: {e}")
                raise

    # If we have a session, yield it and ensure it's closed after use
    if session:
        try:
            yield session
        except sqlalchemy.exc.OperationalError as e:
            # Log any exceptions that occur while the session is being used
            root_cause = str(e.orig) if hasattr(e, "orig") else str(e)
            logger.error(f"Database operation error during session usage: {root_cause}")
            raise  # Re-raise the exception after logging
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
