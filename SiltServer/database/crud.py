from typing import Optional, Type

from sqlalchemy.orm import Session

from SiltServer.models.auth import ModelUser
from SiltServer.models.songs import ModelSong
from SiltServer.schemas.songs import SchemaSongIn


def get_user(db: Session, username: bytes) -> Optional[ModelUser]:
    return db.query(ModelUser).filter(ModelUser.username == username).first()


def get_songs(db: Session) -> list[Type[ModelSong]]:
    return db.query(ModelSong).all()


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
    db.add(db_song)
    db.commit()
    db.refresh(db_song)
    return db_song
