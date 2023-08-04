import secrets
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

from SiltServer.database.crud import get_user
from SiltServer.database.database import get_db

security = HTTPBasic()


def _raise_401():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email and/or password",
        headers={"WWW-Authenticate": "Basic"},
    )


# Must be used in FastAPI function
def authorise(credentials: Annotated[HTTPBasicCredentials, Depends(security)],
              db: Annotated[Session, Depends(get_db)]) -> dict:
    current_username_bytes = credentials.username.encode("utf8")
    current_password_bytes = credentials.password.encode("utf8")

    # Check user exists in the db
    user = get_user(db, current_username_bytes)

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
