from fastapi import status
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.sub import AddSubSchema, SubscriptionResponse
from app.core.models.subscribtion import Subscription
from app.cache.redis import RedisCacheBackend
from app.core.config import settings
from app.parser.parser_service import rss_parser_service
from sqlalchemy import select
from app.crud.sub import get_all_url
from app.core.models.post import Post

async def parse_url(session: AsyncSession, urls: list[SubscriptionResponse]):
    for subscribe in urls:
        print(f"Парсим URL: {subscribe.feed_url}")
        feed = await rss_parser_service.parse_feed([str(subscribe.feed_url)])

        for entry in feed.entries:
            new_post = Post(
                title = entry.title,
                description = entry.description,
                text = entry.link,
                 
            )
        session.add(new_post)
        await session.commit()
