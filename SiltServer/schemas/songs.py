from datetime import date
from typing import Optional

from pydantic import BaseModel


class SchemaSongIn(BaseModel):
    song: str
    album: str
    artist: str
    discog_link: str
    spotify_link: Optional[str]
    youtube_link: Optional[str]
    itunes_link: Optional[str]

    class Config:
        from_attributes = True


class SchemaSongOut(SchemaSongIn):
    id: int
    added_date: date

    class Config:
        from_attributes = True
