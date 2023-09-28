from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from SiltServer.database.crud import get_songs_db, create_song_db
from SiltServer.database.database import get_db
from SiltServer.dependencies.auth import verify_token
from SiltServer.schemas.songs import SchemaSongOut, SchemaSongIn, PaginatedResponse

router = APIRouter(
    dependencies=[],
    prefix="/songs",
    tags=["songs"]
)


@router.get(
    "/",
    summary="Get songs",
    response_model=PaginatedResponse[SchemaSongOut],
    status_code=200)
async def get_songs(
        db: Annotated[Session, Depends(get_db)],
        limit: int = Query(10, ge=1, le=50),
        offset: int = Query(0, ge=0)):
    return get_songs_db(db, limit=limit, offset=offset)


@router.post(
    '/',
    dependencies=[Depends(verify_token)],
    summary="Add a new song",
    response_model=SchemaSongOut,
    status_code=200)
async def post_song(song: SchemaSongIn, db: Annotated[Session, Depends(get_db)]):
    return create_song_db(db, song)
