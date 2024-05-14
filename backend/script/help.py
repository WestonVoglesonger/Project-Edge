from sqlalchemy import create_engine, inspect

engine = create_engine('postgresql://username:password@localhost/dbname')

inspector = inspect(engine)
print(inspector.get_table_names())