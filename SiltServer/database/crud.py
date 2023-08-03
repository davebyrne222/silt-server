from typing import Optional
from sqlalchemy.orm import Session

from models.auth import ModelUser
from models.songs import ModelSong
from schemas.songs import SchemaSongIn


def get_user(db: Session, username: bytes) -> Optional[ModelUser]:
    return db.query(ModelUser).filter(ModelUser.username == username.decode()).first()


def get_songs(db: Session) -> list:
    return db.session.query(ModelSong).all()


def create_song(db: Session, song: SchemaSongIn) -> ModelSong:
    db_song = ModelSong(
        song=song.song,
        album=song.album,
        artist=song.artist,
        discog_link=song.discog_link,
        spotify_link=song.spotify_link,
        youtube_link=song.youtube_link,
        itunes_link=song.itunes_link
    )
    db.session.add(db_song)
    db.session.commit()
    return db_song