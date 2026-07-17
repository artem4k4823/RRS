from fastapi import APIRouter, Depends, Response, Request
from app.deps.dependencies import verify_habr_url
from app.rrs_generator.rrs_generator_service import generate_rss_for_url
from app.rabbitmq.rabbitmq import RabbitMQConsumer
from app.core.config import settings
import urllib.parse

router = APIRouter(prefix='/get-rrs', tags=['RRS-getter'])
rabbitmq = RabbitMQConsumer(settings.RABBIT_URL)

@router.get('/')
async def get_rrs(habr_url: str = Depends(verify_habr_url)):
    rss_xml = await generate_rss_for_url(habr_url)
    
   
    await rabbitmq.publish_json(
        exchange_name="rss.exchange",
        routing_key="rss.result",
        data={
            "url": habr_url, 
            "status": "generated"
        }
    )
    
    
    return Response(content=rss_xml, media_type="application/xml")
