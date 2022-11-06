from email.generator import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./bank_system.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args = {"check_same_thread" : False})

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)
Base = declarative_base()

#Dependency Injection
def get_db() -> Generator:
    try:
        db = SessionLocal() # Created session object
        yield db
    finally:
        db.close()
