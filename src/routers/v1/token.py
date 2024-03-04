from typing import Annotated
from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import IncomingData
from src.models.sellers import Seller
from src.utils.password import verify_password, create_access_token
from src.configurations.database import get_async_session

token_router = APIRouter(tags=["token"], prefix="/token")
DBSession = Annotated[AsyncSession, Depends(get_async_session)]


@token_router.post("/", status_code=status.HTTP_201_CREATED)
async def login_for_access_token(data: IncomingData, session: DBSession):
    e_mail = data.e_mail
    password = data.password
    seller = await session.execute(
        select(Seller).where(Seller.e_mail == e_mail)
    )
    seller = seller.scalars().first()
    if not seller or not verify_password(password, seller.password):
        return Response(status_code=status.HTTP_401_UNAUTHORIZED,
                        content="Incorrect e_mail or password")
    access_token = create_access_token(data={"some": e_mail})

    return {"token": access_token}