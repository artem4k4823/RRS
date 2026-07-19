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
import asyncio
from rabbitmq.rabbitmq import pending_requests
from fastapi.responses import Response


rabbitmq = RabbitMQ(settings.RABBIT_URL)

router = APIRouter(prefix="/generate-rrs-from-url", tags=["RSS-generator"])

from pydantic import BaseModel

class UrlRequest(BaseModel):
    url: str

@router.post('/send-url-for-generate-rss')
async def send_url_to_generator_service(
    session: Annotated[AsyncSession, Depends(db.session_getter)],
    # user: Annotated[User, Depends(get_current_user)],
    body: UrlRequest,
    request: Request
):


    if not is_valid_url(body.url):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail = "Не подходящий URL")
    task_id = str(uuid4())
    event_data = {
        "id": task_id,
        "event":"url.generate.rrs",
        "url": body.url
    }

 
    loop = asyncio.get_running_loop()
    future = loop.create_future()
    pending_requests[task_id] = future

    await rabbitmq.publish_json(
        exchange=request.app.state.URL_GENERATOR_EXCHANGE,
        routing_key = rabbitmq.URL_GENERATOR_ROUTING_KEY,
        data=event_data
    )

    try:
       
        xml_content = await asyncio.wait_for(future, timeout=30.0)
        return Response(content=xml_content, media_type="application/xml")
    except asyncio.TimeoutError:
        raise HTTPException(status.HTTP_504_GATEWAY_TIMEOUT, detail="Timeout waiting for generator service")
    finally:
        pending_requests.pop(task_id, None)

