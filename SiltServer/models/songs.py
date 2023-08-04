from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.sql import func

from SiltServer.database.database import Base


class ModelSong(Base):
    __tablename__ = 'songs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    song = Column(String)
    album = Column(String)
    artist = Column(String)
    discog_link = Column(String)
    spotify_link = Column(String)
    youtube_link = Column(String)
    itunes_link = Column(String)
    added_date = Column(Date(), server_default=func.now())
