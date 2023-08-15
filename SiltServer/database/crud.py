from typing import Optional

from sqlalchemy.orm import Session

from SiltServer.models.auth import ModelUser
from SiltServer.models.songs import ModelSong
from SiltServer.schemas.songs import PaginatedResponse, SchemaSongIn, SchemaSongOut


def get_user(db: Session, username: str) -> Optional[ModelUser]:
    return db.query(ModelUser).filter(ModelUser.username == username).first()


def get_songs(db: Session, limit: int = 1, offset: int = 10) -> PaginatedResponse[SchemaSongOut]:
    results = db.query(ModelSong).offset(offset).limit(limit)
    total = db.query(ModelSong.id).count()
    return PaginatedResponse(
        count=len(list(results)),
        total=total,
        items=results,
        limit=limit,
        offset=offset
    )


def create_song(db: Session, song: SchemaSongIn) -> SchemaSongOut:
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
