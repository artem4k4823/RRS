from fastapi import HTTPException, status
from uuid import uuid4
from app.core.config import settings
from fastapi import APIRouter, Depends, Request
from app.core.database import db
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from rabbitmq.rabbitmq import RabbitMQ
from app.utils.url_validator import is_valid_url
import asyncio
from rabbitmq.rabbitmq import pending_requests
from fastapi.responses import Response
from app.cache.redis import RedisCacheBackend
from app.schemas.url import UrlRequest
from app.utils.async_utils import wait_for_xml_response
from app.utils.url_decoder import encode_url, decode_url

cache = RedisCacheBackend(settings.REDIS_URL, settings.CACHE_TTL_SECONDS)


rabbitmq = RabbitMQ(settings.RABBIT_URL)

router = APIRouter(prefix="/generate-rrs-from-url", tags=["RSS-generator"])



@router.post('/send-url-for-generate-rss')
async def send_url_to_generator_service(
    session: Annotated[AsyncSession, Depends(db.session_getter)],
    body: UrlRequest,
    request: Request
):
    if not is_valid_url(body.url):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Не подходящий URL")
    

    encoded_url = encode_url(body=body)

    base_url = str(request.base_url).rstrip('/')
    rss_link = f"{base_url}{router.prefix}/feed/{encoded_url}"
    
    return {"rss_link": rss_link}


@router.get('/feed/{encoded_url}')
async def get_rss_feed(encoded_url: str, request: Request):
    
    try:
        decoded_data = decode_url(encoded_url=encoded_url)
        original_url = decoded_data["url"]
        pages = decoded_data.get("pages", 1)
    except Exception:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Неверный формат ссылки")

    if not is_valid_url(original_url):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Неверная ссылка")

   
    cached_data = cache.get(encoded_url)
    if cached_data and "xml" in cached_data:
        return Response(content=cached_data["xml"], media_type="application/xml")

    task_id = str(uuid4())
    event_data = {
        "id": task_id,
        "event": "url.generate.rrs",
        "url": original_url,
        "pages": pages
    }
    
    loop = asyncio.get_running_loop()
    future = loop.create_future()
    pending_requests[task_id] = future

    await rabbitmq.publish_json(
        exchange=request.app.state.URL_GENERATOR_EXCHANGE,
        routing_key=rabbitmq.URL_GENERATOR_ROUTING_KEY,
        data=event_data
    )

    xml = await wait_for_xml_response(task_id, future)
    
    cache.set(encoded_url, {"xml": xml})
    
    return Response(content=xml, media_type="application/xml")
