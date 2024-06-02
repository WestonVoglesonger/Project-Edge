from sqlalchemy import create_engine, inspect
import os

# Get database connection details from environment variables
db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_host = os.getenv("POSTGRES_HOST")
db_port = os.getenv("POSTGRES_PORT")
db_name = os.getenv("POSTGRES_DATABASE")

# Create a connection string
connection_string = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

# Create an engine and inspector
engine = create_engine(connection_string)
inspector = inspect(engine)

try:
    # Print the list of tables
    tables = inspector.get_table_names()
    print("Tables in the database:", tables)
except Exception as e:
    print("Error:", e)
