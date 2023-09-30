import logging
from typing import Optional

from sqlalchemy.orm import Session

from SiltServer.models.auth import ModelUser
from SiltServer.models.songs import ModelSong
from SiltServer.schemas.songs import PaginatedResponse, SchemaSongIn, SchemaSongOut

logger = logging.getLogger(__name__)


def get_user_db(db: Session, username: str) -> Optional[ModelUser]:
    logger.debug(f"Getting user with username: {username}")
    return db.query(ModelUser).filter(ModelUser.username == username).first()


def get_songs_db(db: Session, limit: int = 50, offset: int = 0) -> PaginatedResponse:
    logger.debug(f"Getting songs with limit={limit}, offset={offset}")
    results = list(db.query(ModelSong).offset(offset).limit(limit))
    total = db.query(ModelSong.id).count()
    return PaginatedResponse(
        count=len(results),
        total=total,
        items=[SchemaSongOut(**result.__dict__) for result in results],
        limit=limit,
        offset=offset
    )


def create_song_db(db: Session, song: SchemaSongIn) -> SchemaSongOut:
    logger.debug(f"Adding song: {song.model_dump()}")
    song = ModelSong(**song.model_dump())
    db.add(song)
    db.commit()
    db.refresh(song)
    return SchemaSongOut(**song.__dict__)
