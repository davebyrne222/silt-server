from typing import Annotated

from dependencies import authorise
from fastapi import APIRouter, Depends

router = APIRouter(
    dependencies=None,
    prefix="/login",
    tags=["auth"],
)


@router.post(
    "/",
    summary="Validate User Credentials",
    response_model=None,
    status_code=200)
async def login(logon: Annotated[dict, Depends(authorise)]):
    return logon
