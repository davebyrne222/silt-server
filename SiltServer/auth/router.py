from typing import Annotated

from fastapi import APIRouter, Depends

from .dependencies import authorise

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
