from typing import Annotated
from sys import prefix
from fastapi import APIRouter, Depends
from app.core.database import db
from app.crud.user import reg_user
from app.schemas.user import UserCreate
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix='/api/user', tags=['Users'])

@router.post('/register_user')
async def register_user(session: Annotated[AsyncSession, Depends(db.session_getter)], user:UserCreate ):
    user = await reg_user(session = session, username=user.username, password=user.password)
    return user
