from fastapi import APIRouter
from fastapi_sqlalchemy import db

from .models import Song as ModelSong
from .schema import SongOut as SchemaSongOut, SongIn as SchemaSongIn

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
    songs = db.session.query(ModelSong).all()
    return songs


@router.post(
    '/',
    summary="Add a new song",
    response_model=SchemaSongOut,
    status_code=200)
async def post_song(song: SchemaSongIn):
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
