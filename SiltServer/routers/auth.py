from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from SiltServer.database.database import get_db
from SiltServer.dependencies.auth import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from SiltServer.schemas.auth import Token as TokenSchema

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
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        db=db,
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
