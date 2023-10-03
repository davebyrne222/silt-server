import os

from sqlalchemy.orm.session import Session

from SiltServer.database.crud import get_user_db, get_songs_db, create_song_db
from SiltServer.models.auth import ModelUser
from SiltServer.schemas.songs import PaginatedResponse, SchemaSongIn, SchemaSongOut


def test_get_db(db):
    assert isinstance(db, Session)


def test_get_user_db(db):
    user = get_user_db(db, os.getenv("TEST_USERNAME"))
    assert isinstance(user, ModelUser)


def test_get_songs_db(db):
    # Correct response type
    songs = get_songs_db(db)
    assert isinstance(songs, PaginatedResponse)
    assert len(songs.items) > 0
    assert isinstance(songs.items[0], SchemaSongOut)

    # test limit
    songs = get_songs_db(db, limit=10, offset=0)
    assert len(songs.items) == 10

    # test offset works: should be different id to previous test if so
    orig_id = songs.items[0].id
    songs = get_songs_db(db, limit=10, offset=1)
    offset_id = songs.items[0].id
    assert offset_id != orig_id


def test_create_song_db(db):
    song = SchemaSongIn(
        song="test song",
        album="test album",
        artist="test artist",
        discog_link="test link",
        spotify_link=None,
        youtube_link=None,
        itunes_link=None
    )
    created_song = create_song_db(db, song)
    assert isinstance(created_song, SchemaSongOut)
