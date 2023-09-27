from sqlalchemy.orm.session import Session

from SiltServer.database.database import get_db


def test_get_db():
    db = next(get_db())
    assert isinstance(db, Session)
