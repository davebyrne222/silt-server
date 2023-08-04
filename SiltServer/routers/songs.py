from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from SiltServer.database.crud import get_songs, create_song
from SiltServer.database.database import get_db
from SiltServer.dependencies import authorise
from SiltServer.schemas.songs import SchemaSongOut, SchemaSongIn

router = APIRouter(
    dependencies=[],
    prefix="/songs",
    tags=["issues"]
)


@router.get(
    "/",
    summary="Get all songs",
    response_model=None,
    status_code=200)
async def root(db: Annotated[Session, Depends(get_db)]):
    return get_songs(db)


@router.post(
    '/',
    dependencies=[Depends(authorise)],
    summary="Add a new song",
    response_model=SchemaSongOut,
    status_code=200)
async def post_song(song: SchemaSongIn, db: Annotated[Session, Depends(get_db)]) -> SchemaSongOut:
    return create_song(db, song)
