import os
from datetime import timedelta

import pytest
from fastapi import HTTPException
from jose import jwt

from SiltServer.database.database import get_db
from SiltServer.dependencies.auth import authenticate_user, create_access_token, _get_username_from_token
from SiltServer.dependencies.exceptions import raise_401_invalid_creds, raise_401_invalid_token, raise_401_expired_token
from SiltServer.models.auth import ModelUser

# Generic user for testing auth functions
user = ModelUser(
    id=1000,
    username="testuser",
    hash="1234",
    secret="9dded9fc10ecf1f601b605e8b56eba202de7eb5254efd33db4761b8065568a68"
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
    return create_access_token(user, timedelta(15))


def test_create_access_token(token):
    decoded = jwt.decode(token, key=user.secret)
    assert decoded.get("sub") == user.username

def test_get_username_from_token(token):
    username = _get_username_from_token(token)
    assert username == user.username
