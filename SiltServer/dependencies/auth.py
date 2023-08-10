from datetime import datetime, timedelta
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from SiltServer.database.crud import get_user
from SiltServer.database.database import get_db
from SiltServer.models.auth import ModelUser

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# to get a string like this run:
# openssl rand -hex 32
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def _raise_401():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_username_from_token(token: str):
    payload = jwt.decode(token, key=None, options={"verify_signature": False})
    return payload.get("sub")


def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not pwd_context.verify(password, user.hash):
        return False
    return user


def create_access_token(user: ModelUser, expires_delta: Optional[timedelta]):
    # calculate token expiry time
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))

    # set data to be encoded to jwt and return token
    to_encode = {"sub": user.username, "exp": expire}

    return jwt.encode(to_encode, user.secret, algorithm=ALGORITHM)


def verify_token(db: Annotated[Session, Depends(get_db)], token: Annotated[str, Depends(oauth2_scheme)]):
    # get username from token
    current_username = get_username_from_token(token)

    # Get user credentials from DB
    current_user = get_user(db, current_username)

    try:
        payload = jwt.decode(token, current_user.secret, algorithms=[ALGORITHM])

    except JWTError:
        raise _raise_401()
