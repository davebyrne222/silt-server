from fastapi import APIRouter, Depends

from dependencies import authorise
from schemas.songs import SchemaSongOut, SchemaSongIn

from database.crud import get_songs, create_song

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
async def root():
    return get_songs()


@router.post(
    '/',
    dependencies=[Depends(authorise)],
    summary="Add a new song",
    response_model=SchemaSongOut,
    status_code=200)
async def post_song(song: SchemaSongIn) -> SchemaSongOut:
    return create_song(song)
