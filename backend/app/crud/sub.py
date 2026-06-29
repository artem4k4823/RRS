from fastapi import status
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.sub import AddSubSchema, SubscriptionResponse
from app.core.models.subscribtion import Subscription
from app.cache.redis import RedisCacheBackend
from app.core.config import settings
from sqlalchemy import select
import fastfeedparser

cache = RedisCacheBackend(settings.REDIS_URL, settings.CACHE_TTL_SECONDS)

async def get_all_url(session: AsyncSession, user_id: int):
    
    cached_urls = cache.get(settings.URL_CACHED_KEY)
    if cached_urls:
        return [SubscriptionResponse.model_validate(item) for item in cached_urls]
    
    stmt = select(Subscription).where(Subscription.user_id == user_id)
    res = await session.execute(stmt)
    subscriptions = res.scalars().all()
    
    subscriptions_response = [SubscriptionResponse.model_validate(sub) for sub in subscriptions]
    
    urls_for_cache = [sub.model_dump() for sub in subscriptions_response]
    cache.set(settings.URL_CACHED_KEY, urls_for_cache)
    
    return subscriptions_response
    
async def add_feed_url(session: AsyncSession, sub: AddSubSchema, user_id: int):
    try:
        feed = fastfeedparser.parse(sub.url)
        if not feed.get('entries', []):
            raise HTTPException(status_code=400, detail="Невалидный RSS или нет записей")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Не удалось прочитать RSS: {str(e)}")
     
    new_url = Subscription(
        user_id = user_id,
        feed_url = sub.url,
        custom_name = sub.custom_name,
        is_active = True   
    )
    
    urls = await get_all_url(session, user_id=user_id)
    if urls is None:
        urls = []
    if any(u.feed_url == sub.url for u in urls):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail = "Вы уже подписаны на это")
    
    
    cache.delete(settings.URL_CACHED_KEY)
    
    session.add(new_url)
    await session.commit()
    
    
    
    