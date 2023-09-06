import os
from fastapi.testclient import TestClient

from SiltServer.main import app
from SiltServer.schemas.auth import Token
from SiltServer.schemas.songs import PaginatedResponse

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


