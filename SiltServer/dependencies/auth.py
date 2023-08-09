from datetime import datetime, timedelta
import secrets
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from SiltServer.database.crud import get_user
from SiltServer.database.database import get_db

security = HTTPBasic()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "542078bc5fc349b3b499994f6c310270bc5d915c7479ad64a8857984541ce943"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def _raise_401():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email and/or password",
        headers={"WWW-Authenticate": "Basic"},
    )


def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not pwd_context.verify(password, user.hash):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def verify_token(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(get_db)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("verify:", payload)
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception


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
