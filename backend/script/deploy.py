#!/usr/bin/env python3
"""
Deployment script for Project Edge backend.
Handles database migrations and environment setup.
"""

import os
import sys
import subprocess
import argparse
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("deploy")

# Get the project root directory
ROOT_DIR = Path(__file__).parent.parent.parent.absolute()


def run_command(command, cwd=None, capture_output=False):
    """Run a shell command and log the output."""
    try:
        logger.info(f"Running: {command}")
        if cwd is None:
            cwd = ROOT_DIR

        result = subprocess.run(
            command,
            shell=True,
            check=True,
            cwd=cwd,
            capture_output=capture_output,
            text=True,
        )

        if capture_output:
            return result.stdout.strip()
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {command}")
        logger.error(f"Error: {e}")
        if capture_output and e.stdout:
            logger.error(f"stdout: {e.stdout}")
        if e.stderr:
            logger.error(f"stderr: {e.stderr}")
        return False


def check_environment():
    """Check if required environment variables are set."""
    required_vars = [
        "POSTGRES_USER",
        "POSTGRES_PASSWORD",
        "POSTGRES_HOST",
        "POSTGRES_PORT",
        "POSTGRES_DATABASE",
    ]

    missing = [var for var in required_vars if not os.environ.get(var)]

    if missing:
        logger.error(f"Missing environment variables: {', '.join(missing)}")
        return False

    logger.info("Environment check passed")
    return True


def run_migrations():
    """Run alembic migrations."""
    logger.info("Running database migrations")
    return run_command("alembic upgrade head")


def main():
    parser = argparse.ArgumentParser(description="Deployment script for Project Edge")
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Only check environment without making changes",
    )
    parser.add_argument(
        "--skip-migrations", action="store_true", help="Skip database migrations"
    )

    args = parser.parse_args()

    # Check environment
    if not check_environment():
        sys.exit(1)

    if args.check_only:
        logger.info("Environment check completed (check-only mode)")
        sys.exit(0)

    # Run migrations if not skipped
    if not args.skip_migrations:
        if not run_migrations():
            logger.error("Failed to run migrations")
            sys.exit(1)

    logger.info("Deployment completed successfully")


if __name__ == "__main__":
    main()
