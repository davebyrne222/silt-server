from typing import Annotated, List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from SiltServer.database.crud import get_songs, create_song
from SiltServer.database.database import get_db
from SiltServer.dependencies.auth import verify_token
from SiltServer.schemas.songs import SchemaSongOut, SchemaSongIn

router = APIRouter(
    dependencies=[],
    prefix="/songs",
    tags=["songs"]
)


@router.get(
    "/",
    summary="Get all songs",
    response_model=List[SchemaSongOut],
    status_code=200)
async def root(
        db: Annotated[Session, Depends(get_db)],
        limit: int = Query(1, ge=1),
        offset: int = Query(10, ge=0)):
    return get_songs(db, limit=limit, offset=offset)


@router.post(
    '/',
    dependencies=[Depends(verify_token)],
    summary="Add a new song",
    response_model=SchemaSongOut,
    status_code=200)
async def post_song(song: SchemaSongIn, db: Annotated[Session, Depends(get_db)]):
    return create_song(db, song)
