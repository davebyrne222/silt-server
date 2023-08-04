from typing import Optional, List

from sqlalchemy.orm import Session

from SiltServer.models.auth import ModelUser
from SiltServer.models.songs import ModelSong
from SiltServer.schemas.songs import SchemaSongIn


def get_user(db: Session, username: bytes) -> Optional[ModelUser]:
    return db.query(ModelUser).filter(ModelUser.username == username.decode()).first()


def get_songs(db: Session) -> List[ModelSong]:
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
