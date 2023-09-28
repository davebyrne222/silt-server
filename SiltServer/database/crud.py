from typing import Optional

from sqlalchemy.orm import Session

from SiltServer.models.auth import ModelUser
from SiltServer.models.songs import ModelSong
from SiltServer.schemas.songs import PaginatedResponse, SchemaSongIn, SchemaSongOut


def get_user(db: Session, username: str) -> Optional[ModelUser]:
    return db.query(ModelUser).filter(ModelUser.username == username).first()


def get_songs(db: Session, limit: Optional[int] = None, offset: int = 0) -> PaginatedResponse:
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
    song = ModelSong(**song.__dict__)
    db.add(song)
    db.commit()
    db.refresh(song)
    return SchemaSongOut(**song.__dict__)
