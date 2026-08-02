from aio_pika import message
from app.core.models import User
from fastapi import APIRouter, Depends
from app.core.database import db
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.schemas.oprional_url import OptionalUrlSchema
from app.crud.url_list import add_optional_url, delete_optional_url, get_all_optional_url
from app.auth.dependencies import get_current_user, isAdmin

router = APIRouter(prefix="/optional_url_list", tags=['optional-urls'])

@router.get('/get-all-optionals-urls')
async def get_all_optionals_urls(
    session: Annotated[AsyncSession, Depends(db.session_getter)],
    user: Annotated[User, Depends(get_current_user)],
   
):
    result = await get_all_optional_url(session=session)
    return result


@router.post('/add-url-to-optional')
async def add_url_to_optional(
    session: Annotated[AsyncSession, Depends(db.session_getter)],
    user: Annotated[User, Depends(get_current_user)],
    isAdmin: Annotated[User, Depends(isAdmin)],
    url: OptionalUrlSchema
):
    await add_optional_url(session=session, optional_url=url)
    return {"message":"ссылка создана успеншно"}

@router.delete('/delete-optional-url')
async def delete_optional_url(
    session: Annotated[AsyncSession, Depends(db.session_getter)],
    user: Annotated[User, Depends(get_current_user)],
    isAdmin: Annotated[User, Depends(isAdmin)],
    url_id: int
):
    await delete_optional_url(session=session, url_id=url_id)
    return {"message":"ссылка успеншно удалена"}