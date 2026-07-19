from uuid import uuid4
from app.core.config import settings
from app.crud.post import create_post_crud, get_all_posts_crud
from fastapi import APIRouter, Depends, Request
from app.core.database import db
from app.core.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.post import PostSchema
from typing import Annotated
from rabbitmq.rabbitmq import RabbitMQ

from app.auth.dependencies import get_current_user

router = APIRouter(prefix='/posts', tags=['Posts'])

rabbitmq = RabbitMQ(settings.RABBIT_URL)

@router.get('/get-all-post')
async def get_all_posts(
    session: Annotated[AsyncSession, Depends(db.session_getter)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    posts = await get_all_posts_crud(session=session)
    return posts


@router.post('/create-post')
async def create_post(
    session: Annotated[AsyncSession, Depends(db.session_getter)],
    current_user: Annotated[User, Depends(get_current_user)],
    post: PostSchema,
    request: Request
):
    created_post = await create_post_crud(session=session, post=post, user_id=current_user.id)

    # event_data ={
    #         "id": str(uuid4()),
    #         "event": "post.create",
    #         "title": created_post.title,
    #        }

    # await rabbitmq.publish_json(
    #     exchange=request.app.state.URL_GENERATOR_EXCHANGE,
    #     routing_key=rabbitmq.URL_GENERATOR_ROUTING_KEY,
    #     data=event_data
    # )
    return created_post
    