import pytest

from SiltServer.database.database import get_db


@pytest.fixture(name="db")
def get_db_instance():
    return next(get_db())