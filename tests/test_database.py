import pytest
from sqlalchemy.orm.session import Session

from SiltServer.database.crud import get_user
from SiltServer.database.database import get_db
from SiltServer.models.auth import ModelUser


@pytest.fixture(name="db")
def get_db_instance():
    return next(get_db())


def test_get_db(db):
    assert isinstance(db, Session)


def test_get_user(db):
    user = get_user(db, 'davebyrne')
    assert isinstance(user, ModelUser)
