from datetime import datetime, timedelta
from typing import Annotated, Optional

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from SiltServer.database.crud import get_user
from SiltServer.database.database import get_db
from SiltServer.dependencies.exceptions import raise_401_expired_token, raise_401_invalid_token
from SiltServer.models.auth import ModelUser

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# to get a string like this run:
# openssl rand -hex 32
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1


def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not pwd_context.verify(password, user.hash):
        return False
    return user


def create_access_token(user: ModelUser, expires_delta: Optional[timedelta]):
    # calculate token expiry time
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    # set data to be encoded to jwt and return token
    to_encode = {"sub": user.username, "exp": expire}

    return jwt.encode(to_encode, user.secret, algorithm=ALGORITHM)


def _get_username_from_token(token: str):
    payload = jwt.decode(token, key="", options={"verify_signature": False})
    return payload.get("sub")


def verify_token(db: Annotated[Session, Depends(get_db)], token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        # get username from token
        current_username = _get_username_from_token(token)

        # Get user credentials from DB
        current_user = get_user(db, current_username)

        # Attempt to decode: invalid token if error raised
        jwt.decode(token, current_user.secret, algorithms=[ALGORITHM])

    except ExpiredSignatureError:
        raise_401_expired_token()

    except JWTError:
        raise raise_401_invalid_token()
