from fastapi import APIRouter, Depends
from app.core.database import db
from app.core.models import User
from app.schemas.sub import AddSubSchema
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.crud.sub import get_all_url, add_feed_url, delete_sub

from app.auth.dependencies import get_current_user

router = APIRouter(prefix='/subscriptions', tags=['Subs'])


@router.get('/get-all-subs')
async def get_all_subs(
    session: Annotated[AsyncSession, Depends(db.session_getter)],
    current_user: Annotated[User, Depends(get_current_user)]):
    urls = await get_all_url(session=session, user_id=current_user.id)
    return urls


@router.post('/add-subs')
async def add_subs(
    session: Annotated[AsyncSession, Depends(db.session_getter)],
    current_user: Annotated[User, Depends(get_current_user)],
    url: AddSubSchema
    ):
    await add_feed_url(session=session, sub=url, user_id=current_user.id)
    return {"message": "Успешно добавлено"}


@router.delete('/delete-sub/{sub_id}')
async def delete_user_sub(
    session: Annotated[AsyncSession, Depends(db.session_getter)],
    current_user: Annotated[User, Depends(get_current_user)],
    sub_id: int
):
    await delete_sub(session=session, sub_id=sub_id, user_id=current_user.id)
    return {"message": "Подписка была удалена"}




    
    

