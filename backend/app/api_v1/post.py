from app.crud.post import create_post_crud, get_all_posts_crud
from fastapi import APIRouter, Depends
from app.core.database import db
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.post import PostSchema
from typing import Annotated

router = APIRouter(prefix='/api/posts', tags=['Posts'])


@router.get('/get-all-post')
async def get_all_posts(session: Annotated[AsyncSession, Depends(db.session_getter)]):
    posts  = await get_all_posts_crud(session=session)
    return posts


@router.post('/create-post')
async def create_post(session:Annotated[AsyncSession, Depends(db.session_getter)], post: PostSchema):
    post = await create_post_crud(session=session, post = post)
    return post
    