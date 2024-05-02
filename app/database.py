from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg
import time
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# create an engine. engine is responsible for SQLAlchemy to connect to the database.

engine= create_engine(SQLALCHEMY_DATABASE_URL)

# To talk to database, we need to create a session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:

#     try:
#         conn = psycopg.connect(host='localhost' , dbname='fastapi', user='postgres', password='1234', row_factory=psycopg.rows.dict_row)
#         cursor= conn.cursor()
#         print("Database connection was Successful")
#         break
#     except Exception as error:
#         print("Connecting to database failed.")
#         print("Error",error)
#         time.sleep(2)


#Tables can be created as models