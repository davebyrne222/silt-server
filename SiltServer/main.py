import os

import uvicorn
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db
from pydantic_settings import BaseSettings

from models import Song as ModelSong
from schema import SongOut as SchemaSongOut, SongIn as SchemaSongIn


class Settings(BaseSettings):
    """Loads from .env"""
    SERVER_ADDR_HOST: str = "0.0.0.0"
    SERVER_ADDR_PORT: int = 8081
    SERVER_RELOAD: bool = False


settings = Settings()

app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])


# app.include_router(auth_router.router)
# app.include_router(issues_router.router)


@app.get("/")
async def root():
    songs = db.session.query(ModelSong).all()
    return songs


@app.post('/song/', response_model=SchemaSongOut)
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


if __name__ == "__main__":
    print(settings.model_dump())

    uvicorn.run("main:app",
                host=settings.SERVER_ADDR_HOST,
                port=settings.SERVER_ADDR_PORT,
                reload=settings.SERVER_RELOAD
                )
