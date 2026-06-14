from app.schemas.user import UserLogin
from app.core.config import settings
from app.core.models import User
from fastapi import APIRouter, Depends, Response, Request, HTTPException, status
from app.crud.auth import log_user, refresh_tokens_crud

from app.core.database import db
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.token import RefreshTokenRequest, TokenResponse
from app.auth.dependencies import get_current_user

router = APIRouter(prefix='/auth', tags=['Auth'])

@router.post('/login', response_model=TokenResponse)
async def login_user(
    session: Annotated[AsyncSession, Depends(db.session_getter)],
    user: UserLogin,
):
    tokens = await log_user(
        session=session,
        ent_username=user.username,
        ent_password=user.password,
    )
    return tokens


@router.post('/refresh', response_model=TokenResponse)
async def refresh_tokens(  
    session: Annotated[AsyncSession, Depends(db.session_getter)],
    refresh_data: RefreshTokenRequest,
):
    new_access_token, new_refresh_token = await refresh_tokens_crud(
        session=session, 
        refresh_data=refresh_data,
    )
    
    return TokenResponse(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
    )


@router.get('/me')
async def get_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    
    return {
        "id": current_user.id,
        "username": current_user.username,
        "isCreator": current_user.isCreator,
        "isAdmin": current_user.isAdmin,
        "status": current_user.status,
    }