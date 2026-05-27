from fastapi import APIRouter,Depends
from app.crud.auth import log_user
from app.schemas.user import UserCreate
from app.core.database import db
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix='/auth', tags=['Auth'])

@router.post('/login')
async def login_user(session: Annotated[AsyncSession, Depends(db.session_getter)], user: UserCreate):
    await log_user(session=session, ent_username= user.username, ent_password=user.password)
