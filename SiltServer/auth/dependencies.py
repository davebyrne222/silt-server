import secrets
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi_sqlalchemy import db

from .models import UserModel

security = HTTPBasic()


def get_user(username: bytes) -> Optional[UserModel]:
    return db.session.query(UserModel).filter(UserModel.username == username.decode()).first()


def _raise_401():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email and/or password",
        headers={"WWW-Authenticate": "Basic"},
    )


def authorise(credentials: Annotated[HTTPBasicCredentials, Depends(security)]) -> dict:
    current_username_bytes = credentials.username.encode("utf8")
    current_password_bytes = credentials.password.encode("utf8")

    # Check user exists in the db
    user = get_user(current_username_bytes)

    if not user:
        _raise_401()

    # check username
    is_correct_username = secrets.compare_digest(
        current_username_bytes, user.username.encode()
    )

    # check password
    is_correct_password = secrets.compare_digest(
        current_password_bytes, user.hash.encode()
    )

    # check both are correct
    if not (is_correct_username and is_correct_password):
        _raise_401()

    return {"login": "success"}
