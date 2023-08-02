from datetime import date

from pydantic import BaseModel


class Song(BaseModel):
    id: int
    song: str
    album: str
    artist: str
    discog_link: str
    spotify_link: str = None
    youtube_link: str = None
    itunes_link: str = None
    added_date: date

    class Config:
        orm_mode = True
