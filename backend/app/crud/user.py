from app.core.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.auth.auth_helper import hash_password
from fastapi import HTTPException, status

async def get_user_by_username(session: AsyncSession, username: str):
    stmt = select(User).where(User.username == username)
    res = await session.execute(stmt)
    result = res.scalar_one_or_none()   
    if not result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail= "Такого пользователя нету")
    return result
        

    