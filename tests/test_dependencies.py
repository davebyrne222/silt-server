import pytest
from fastapi import HTTPException

from SiltServer.dependencies.exceptions import raise_401_invalid_creds, raise_401_invalid_token, raise_401_expired_token


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
