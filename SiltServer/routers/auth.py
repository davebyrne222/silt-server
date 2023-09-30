from datetime import timedelta
import logging
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from SiltServer.database.database import get_db
from SiltServer.dependencies.auth import authenticate_user, create_access_token
from SiltServer.dependencies.exceptions import raise_401_invalid_creds
from SiltServer.schemas.auth import Token as TokenSchema

logger = logging.getLogger(__name__)

router = APIRouter(
    dependencies=[],
    prefix="/token",
    tags=["auth"]
)


@router.post(
    "/",
    summary="Login to receive JWT Token",
    response_model=TokenSchema,
    status_code=200
)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_db)]):
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise_401_invalid_creds()

    access_token = create_access_token(
        expires_delta=timedelta(minutes=15),
        user=user
    )

    logger.debug(f"Token Created: {access_token}")

    return {"access_token": access_token, "token_type": "bearer"}
