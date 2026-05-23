from app.core.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.auth.auth_helper import hash_password

async def reg_user(session:AsyncSession, username: str, password: str):
    password = hash_password(password)
    user = User(
        username = username,
        password = password,
    )
        
    session.add(user)
    await session.commit()
    return user



