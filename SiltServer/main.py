import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db

from models import Song as ModelSong
from schema import SongOut as SchemaSongOut, SongIn as SchemaSongIn

load_dotenv('.env')

app = FastAPI()

app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])


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


# To run locally
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
