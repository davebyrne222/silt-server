from sqlalchemy import Column, Integer, String

from database.database import Base


class ModelUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    hash = Column(String)
