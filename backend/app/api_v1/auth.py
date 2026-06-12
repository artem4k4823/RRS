from app.schemas.user import UserLogin
from app.core.config import settings
from fastapi import APIRouter,Depends, Response, Request
from app.crud.auth import log_user
from app.schemas.user import UserCreate
from app.core.database import db
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix='/auth', tags=['Auth'])

@router.post('/login')
async def login_user(response: Response, session: Annotated[AsyncSession, Depends(db.session_getter)], user: UserLogin):
    access_token = await log_user(session=session, ent_username= user.username, ent_password=user.password)
    response.set_cookie(
        key = 'access_token',
        value=access_token,
        httponly=True,
        secure=False,
        samesite='lax',
        max_age = settings.ACCCESS_TOKEN_EXPIRE_MINUTES * 60,
        path = '/'
        
    )
    return {
        'message': 'login succesful',
        'user_id': user.username,
        'access_token': access_token
        
    }