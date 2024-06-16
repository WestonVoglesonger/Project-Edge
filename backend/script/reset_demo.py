import sys
import subprocess
from sqlalchemy.orm import Session
from backend.entities.base import Base
from backend.test.services.demo_data import user_data
from backend.test.services.demo_data import discussion_data, project_data
from ..database import engine
from ..env import getenv
from ..entities.user_entity import UserEntity  # Ensure all your entities are imported

__authors__ = ["Kris Jordan", "Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

if getenv("MODE") != "development":
    print("This script can only be run in development mode.", file=sys.stderr)
    print("Add MODE=development to your .env file in workspace's `backend/` directory")
    exit(1)

# Run Delete and Create Database Scripts
subprocess.run(["python3", "-m", "backend.script.delete_database"])
subprocess.run(["python3", "-m", "backend.script.create_database"])

# Reset Tables
print("Dropping all tables...")
Base.metadata.drop_all(engine)
print("Creating all tables...")
Base.metadata.create_all(engine)
print("Tables created successfully.")

# Initialize the SQLAlchemy session
with Session(engine) as session:
    user_data.insert_fake_data(session)
    project_data.insert_fake_data(session)
    discussion_data.insert_fake_data(session)
    session.commit()
