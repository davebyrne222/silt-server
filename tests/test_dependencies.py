import os
from datetime import timedelta

import pytest
from fastapi import HTTPException
from jose import jwt

from SiltServer.database.database import get_db
from SiltServer.dependencies.auth import authenticate_user, create_access_token, verify_token
from SiltServer.dependencies.exceptions import raise_401_invalid_creds, raise_401_invalid_token, raise_401_expired_token
from SiltServer.models.auth import ModelUser

# Generic user for testing auth functions
USER = ModelUser(
    id=1000,
    username="davebyrne",
    hash="1234",
    secret="542078bc5fc349b3b499994f6c310270bc5d915c7479ad64a8857984541ce943"
)


def test_raise_401_invalid_creds():
    with pytest.raises(HTTPException) as exc:
        raise_401_invalid_creds()
    assert exc.value.detail == "Incorrect username or password"


def test_raise_401_invalid_token():
    with pytest.raises(HTTPException) as exc:
        raise_401_invalid_token()
    assert exc.value.detail == "Could not validate token"


def test_raise_401_expired_token():
    with pytest.raises(HTTPException) as exc:
        raise_401_expired_token()
    assert exc.value.detail == "Token has expired"


def test_authenticate_user():
    db = next(get_db())  # generator function. Need to invoke yield
    username = os.getenv("TEST_USERNAME")
    pwd = os.getenv("TEST_PASSWORD")
    user = authenticate_user(db, username, pwd)
    assert user


@pytest.fixture(name="token")
def get_jwt_token():
    return create_access_token(USER, timedelta(15))


def test_create_access_token(token):
    decoded = jwt.decode(token, key=USER.secret)
    assert decoded.get("sub") == USER.username


def test_verify_token_success(token):
    db = next(get_db())
    assert not verify_token(db, token)


def test_verify_token_invalid_username():
    """Test to ensure username decoded from JWT is valid i.e. a user in the database"""
    db = next(get_db())

    invalid_user = ModelUser(
        id=USER.id,
        username="testuser",
        hash=USER.hash,
        secret=USER.secret
    )

    token = create_access_token(invalid_user, timedelta(15))

    with pytest.raises(HTTPException) as exc:
        verify_token(db, token)

    assert exc.value.detail == "Could not validate token"


def test_verify_token_invalid_token():
    db = next(get_db())
    with pytest.raises(HTTPException) as exc:
        verify_token(db, "faketoken")
    assert exc.value.detail == "Could not validate token"


def test_verify_token_expired_token():
    db = next(get_db())
    token = create_access_token(USER, timedelta(-15))
    with pytest.raises(HTTPException) as exc:
        verify_token(db, token)
    assert exc.value.detail == "Token has expired"
