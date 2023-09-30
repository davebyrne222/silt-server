import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

logger = logging.getLogger(__name__)

# DB connection / interface
DB_URL = os.environ['POSTGRES_TEST_URL'] if os.environ['TESTING'] == '1' else os.environ['POSTGRES_URL']

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()


# dependency for routes
def get_db():
    logger.debug(f"Getting database session envar TESTING={os.environ('TESTING')}")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
