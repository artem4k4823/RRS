from fastapi import HTTPException, status
from fastapi import APIRouter, Depends
from app.core.database import db
from app.core.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.auth.dependencies import get_current_user
from app.schemas.user import UserSchema, UserWithSubsSchema
from app.crud.admin_operations import get_user_by_id, get_user_with_urls, ban_user, unban_user, delete_sub_of_user


router = APIRouter(prefix="/admin-operations", tags=['Admin'])


@router.get('/get-user-by-id')
async def get_some_user_by_id(
    session: Annotated[AsyncSession, Depends(db.session_getter)],
    user: Annotated[User, Depends(get_current_user)],
    user_id: int
) -> UserSchema:
    if not user.isAdmin:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail = "Требует прав администратора")
    user = await get_user_by_id(session=session, user_id=user_id)
    result = UserSchema.model_validate(user)
    return result


@router.patch('/ban-user')
async def ban_some_user(
    session: Annotated[AsyncSession, Depends(db.session_getter)],
    user: Annotated[User, Depends(get_current_user)],
    user_id: int
):
    if not user.isAdmin:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail = "Требует прав администратора")
    res = await ban_user(session=session, user_id=user_id)
    return res


@router.patch('/unban-user')
async def unban_some_user(
    session: Annotated[AsyncSession, Depends(db.session_getter)],
    user: Annotated[User, Depends(get_current_user)],
    user_id: int
):
    if not user.isAdmin:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail = "Требует прав администратора")
    res = await unban_user(session=session, user_id=user_id)
    return res


@router.get('/get-users-with-subs')
async def get_some_users_with_subs(
    session: Annotated[AsyncSession, Depends(db.session_getter)],
    user: Annotated[User, Depends(get_current_user)],
    user_id: int
) -> UserWithSubsSchema:
    if not user.isAdmin:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Требует прав администратора")
    db_user = await get_user_with_urls(session=session, user_id=user_id)
    result = UserWithSubsSchema.model_validate(db_user)
    return result
    

@router.delete('/delete-user-sub')
async def delete_user_sub(
    session: Annotated[AsyncSession, Depends(db.session_getter)],
    user: Annotated[User, Depends(get_current_user)],
    user_id: int,
    sub_id: int
):
    if not user.isAdmin:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail = "Требует прав администратора")
    res = await delete_sub_of_user(session=session, user_id=user_id,sub_id= sub_id)
    return res

