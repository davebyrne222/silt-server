import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DB connection / interface
engine = create_engine(os.environ['DATABASE_URL'])

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()


# dependency for routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
