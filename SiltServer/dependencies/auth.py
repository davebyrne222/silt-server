from datetime import datetime, timedelta
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from SiltServer.database.crud import get_user

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


def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not pwd_context.verify(password, user.hash):
        return False
    return user


def create_access_token(db, data: dict, expires_delta: Optional[timedelta]):
    # TODO: get active user
    current_username = 'davebyrne'
    SECRET = get_user(db, current_username).secret

    # calculate token expiry time
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))

    # set data to be encoded to jwt and return token
    to_encode = data.copy() | {"exp": expire}

    return jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)


async def verify_token(db, token: Annotated[str, Depends(oauth2_scheme)]):
    # TODO: get active user
    current_username = 'davebyrne'

    # Get user credentials from DB
    current_user = get_user(db, current_username)

    try:
        payload = jwt.decode(token, current_user.secret, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username != current_user.username:
            raise _raise_401()

    except JWTError:
        raise _raise_401()
