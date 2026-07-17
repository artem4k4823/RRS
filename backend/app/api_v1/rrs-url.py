from fastapi import HTTPException, status
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
from app.utils.url_validator import is_valid_url

rabbitmq = RabbitMQ(settings.RABBIT_URL)

router = APIRouter(prefix="/generate-rrs-from-url", tags=["RRS-generator"])

async def send_url_to_generator_service(
    session: Annotated[AsyncSession, Depends(db.session_maker)],
    user: Annotated[User, Depends(get_current_user)],
    url: str,
    request: Request
):


    if not is_valid_url(url):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail = "Не подходящий URL")
    event_data = {
        "id": str(uuid4()),
        "event":"url.generate.rrs",
        "url": url
    }

    await rabbitmq.publish_json(
        exchange=request.app.state.URL_GENERATOR_EXCHANGE,
        routing_key = rabbitmq.URL_GENERATOR_ROUTING_KEY,
        data=event_data
    )