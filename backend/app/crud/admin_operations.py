from app.core.models import Subscription
from app.core.models import Post
from app.core.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from app.auth.auth_helper import hash_password
from fastapi import HTTPException, status


async def get_user_by_username(session: AsyncSession, username: str) -> User:
    stmt = select(User).where(User.username == username)
    res = await session.execute(stmt)
    result = res.scalar_one_or_none()   
    if not result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail= "Пользователь не найден")
    return result


async def get_user_by_id(session: AsyncSession, user_id: int) -> User:
    stmt = select(User).where(User.id == user_id)
    res = await session.execute(stmt)
    result = res.scalar_one_or_none()
    if not result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail = "Пользователь не найден")
    return result


async def get_user_with_urls(session: AsyncSession, user_id: int) -> User:
    stmt = select(User).options(selectinload(User.subscriptions)).where(User.id == user_id)
    res = await session.execute(stmt)
    result = res.scalar_one_or_none()
    if not result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    return result


async def ban_user(session: AsyncSession, user_id: int) -> dict:
    user = await get_user_by_id(session=session, user_id=user_id)
    if user.isAdmin:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Пользователь является администратором")
    if not user.status:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail = "Пользователь уже заблокирован")
    user.status = False
    await session.commit()
    return {"message": "Пользователь был заблокирован"}


async def unban_user(session: AsyncSession, user_id: int) -> dict:
    user = await get_user_by_id(session=session, user_id=user_id)
    if user.status:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Пользователь не заблокирован")
    user.status = True
    await session.commit()
    return {"message": "Пользователь разблокирован"}


async def delete_sub_of_user(session: AsyncSession, user_id: int, sub_id: int) -> dict:
    user = await get_user_with_urls(session=session, user_id=user_id)
    
    subscription = None
    for sub in user.subscriptions:
        if sub.id == sub_id:
            subscription = sub
            break
            
    if not subscription:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Подписка не найдена у данного пользователя")
        
    await session.delete(subscription)
    await session.commit()
    return {"message": "У пользователя была удалена подписка"}


