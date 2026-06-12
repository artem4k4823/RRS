from app.core.models import RefreshToken
from app.auth.token import create_refresh_token
from app.auth.token import create_access_token
from app.core.models import User
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.auth.auth_helper import hash_password, verify_password
from .user import get_user_by_username
from app.core.config import settings
from datetime import datetime, timedelta

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
    access_token = create_access_token(user_id=user.id)
    refresh_token = create_refresh_token(user_id=user.id)
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_EXPIRE_TIME_DAYS)
    db_refresh_token = RefreshToken(
        token = refresh_token,
        user_username = user.username,
        expire_at = expire 
    )
    session.add(db_refresh_token)
    await session.commit()
    return {
        access_token
    }
        
        
        
    