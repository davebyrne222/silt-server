from sqlalchemy.orm.session import Session

from SiltServer.database.crud import get_user
from SiltServer.models.auth import ModelUser


def test_get_db(db):
    assert isinstance(db, Session)


def test_get_user(db):
    user = get_user(db, 'davebyrne')
    assert isinstance(user, ModelUser)
