from fastapi.testclient import TestClient

from SiltServer.main import app
from SiltServer.schemas.songs import PaginatedResponse

client = TestClient(app)


def test_get_songs():
    response = client.get("/songs")
    assert response.status_code == 200

    # Validate response against Pydantic model
    try:
        PaginatedResponse(**response.json())
    except ValueError as e:
        assert False, f"Response structure does not match the Pydantic model: {e}"

    assert True
