from app.auth.token import create_access_token
from app.core.models import User
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.auth.auth_helper import hash_password, verify_password
from .user import get_user_by_username

async def reg_user(session:AsyncSession, username: str, password: str) -> User:
    password = hash_password(password)
    user = User(
        username = username,
        password = password,
    )

    session.add(user)
    await session.commit()
    return user

async def log_user(session: AsyncSession, ent_username: str, ent_password: str):
    user = await get_user_by_username(session, ent_username)
    if not verify_password(ent_password, user.password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail = 'Неверный логин или пароль')
    acces_token = await create_access_token(session = session, user_id=user.id, user_data = {'sub': user.username})
    refresh_token = ...
    return {
        'acces_token': acces_token,
        'refresh_token': refresh_token
    }
        
        
        
    