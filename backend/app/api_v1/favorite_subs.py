from fastapi import APIRouter, Depends
from app.core.database import db
from app.core.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.auth.dependencies import get_current_user
from app.crud.favorite_subs_crud import (
    add_to_favorite,
    delete_from_favorites,
    get_all_user_favorite_urls
)

router = APIRouter(prefix="/favorites", tags=['Favorites'])


@router.get('/get-all-favorites')
async def get_all_favorites(
    session: Annotated[AsyncSession, Depends(db.session_getter)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    result = await get_all_user_favorite_urls(session=session, user_id=current_user.id)
    return result


@router.post('/add-to-favorite/{url_id}')
async def add_favorite(
    session: Annotated[AsyncSession, Depends(db.session_getter)],
    current_user: Annotated[User, Depends(get_current_user)],
    url_id: int
):
    res = await add_to_favorite(session=session, user_id=current_user.id, url_id=url_id)
    return res


@router.delete('/delete-from-favorite/{url_id}')
async def delete_favorite(
    session: Annotated[AsyncSession, Depends(db.session_getter)],
    current_user: Annotated[User, Depends(get_current_user)],
    url_id: int
):
    res = await delete_from_favorites(session=session, url_id=url_id, user_id=current_user.id)
    return res
