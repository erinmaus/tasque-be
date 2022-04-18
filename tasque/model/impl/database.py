from os import environ
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

TASQUE_DATABASE_URL = environ.get("TASQUE_DATABASE_URL")
TASQUE_DATABASE_USERNAME = environ.get("TASQUE_DATABASE_USERNAME")
TASQUE_DATABASE_PASSWORD = environ.get("TASQUE_DATABASE_PASSWORD")
TASQUE_DATABASE_HOST = environ.get("TASQUE_DATABASE_HOST")
TASQUE_DATABASE_PORT = environ.get("TASQUE_DATABASE_PORT")
TASQUE_DATABASE = environ.get("TASQUE_DATABASE")
TASQUE_DATABASE_CONNECTION_URL = environ.get("DATABASE_URL", None)

url = TASQUE_DATABASE_CONNECTION_URL or URL.create(
    drivername="postgresql",
    username=TASQUE_DATABASE_USERNAME,
    password=TASQUE_DATABASE_PASSWORD,
    host=TASQUE_DATABASE_HOST,
    port=TASQUE_DATABASE_PORT,
    database=TASQUE_DATABASE,
)

engine = create_engine(url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
