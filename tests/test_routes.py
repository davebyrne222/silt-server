import os
from fastapi.testclient import TestClient
import pytest

from SiltServer.main import app
from SiltServer.schemas.auth import Token
from SiltServer.schemas.songs import PaginatedResponse, SchemaSongOut

client = TestClient(app)


def assert_valid_response(model, json):
    try:
        model(**json)
    except ValueError as e:
        assert False, f"Response structure does not match the Pydantic model: {e}"

    assert True


def test_get_songs():
    response = client.get("/songs")

    assert response.status_code == 200

    # Validate response against Pydantic model
    assert_valid_response(PaginatedResponse, response.json())


def test_login_failure():
    response = client.post("/token", data=dict(username="none", password="none"))
    assert response.status_code == 401


def test_login_success():

    response = client.post("/token",
                           data=dict(
                               username=f"{os.getenv('TEST_USERNAME')}",
                               password=f"{os.getenv('TEST_PASSWORD')}"
                                    )
                           )
    assert response.status_code == 200

    assert_valid_response(Token, response.json())

    return response.json().get("access_token")


@pytest.fixture(name="token")
def get_token():
    response = client.post("/token",
                           data=dict(
                               username=f"{os.getenv('TEST_USERNAME')}",
                               password=f"{os.getenv('TEST_PASSWORD')}"
                           )
                           )

    return response.json().get("access_token")

def test_add_songs(token):
    header = dict(Authorization=f"Bearer {token}")

    body = dict(
        song="test song",
        album="test album",
        artist="test artist",
        discog_link="test discog_link",
        spotify_link="test spotify_link",
        youtube_link="test youtube_link",
        itunes_link="test itunes_link"
    )

    response = client.post("/songs",
                           headers=header,
                           json=body
                           )

    assert response.status_code == 200

    assert_valid_response(SchemaSongOut, response.json())
