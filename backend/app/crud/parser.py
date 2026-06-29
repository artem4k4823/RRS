from datetime import datetime
import time
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
            link = entry.get('link')
            if not link:
                continue
            
            stmt = select(Post).where(Post.link == link)
            res = await session.execute(stmt)
            if res.scalar() is not None:
                continue

            published_at = None
            published_parsed = entry.get('published_parsed') or entry.get('updated_parsed')
            if published_parsed:
                try:
                    published_at = datetime.fromtimestamp(time.mktime(published_parsed))
                except Exception:
                    pass

            new_post = Post(
                title = entry.get('title', ''),
                link = link,
                summary = entry.get('summary') or entry.get('description'),
                published_at = published_at,
                feed_id = subscribe.id,
                user_id = subscribe.user_id,
            )
            session.add(new_post)
        
        await session.commit()
