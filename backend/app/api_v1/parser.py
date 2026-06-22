from fastapi import APIRouter, Depends
from app.core.database import db
from app.core.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.crud.parser import parse_url
from app.auth.dependencies import get_current_user
from app.crud.sub import get_all_url

router = APIRouter(prefix='/parser', tags=['Parser'])

@router.post('/parse')
async def parse_some_url(session: Annotated[AsyncSession, Depends(db.session_getter)], user: Annotated[User, Depends(get_current_user)]):
    urls = await get_all_url(session=session, user_id=user.id)
    await parse_url(session=session, urls=urls)
    return "удачно"
    
    