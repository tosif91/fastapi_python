# Integrating sqlite to save data in the database

from sqlalchemy.engine import create_engine  # engine to interact with database
from sqlalchemy.orm import sessionmaker  # orm and session
from sqlalchemy.ext.declarative import declarative_base  # base class
from starlette.config import Config


config = Config(".env")

SQLALCHEMY_DATABASE_URL = config("SQLALCHEMY_DATABASE_URL")


engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                       'check_same_thread': False})

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
