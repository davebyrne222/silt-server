from fastapi.testclient import TestClient

from SiltServer.main import app

client = TestClient(app)


def test_get_songs():
    response = client.get("/songs")
    assert response.status_code == 200
    # assert response.json() == {
    #     "id": "foo",
    #     "title": "Foo",
    #     "description": "There goes my hero",
    # }