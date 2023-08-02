from datetime import date

from pydantic import BaseModel


class SongIn(BaseModel):
    song: str
    album: str
    artist: str
    discog_link: str
    spotify_link: str = None
    youtube_link: str = None
    itunes_link: str = None

    class Config:
        orm_mode = True


class SongOut(SongIn):
    id: int
    added_date: date

    class Config:
        orm_mode = True
