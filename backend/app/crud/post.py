from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.post import PostSchema
from app.core.models.post import Post
from app.schemas.post import PostSchema
from app.cache.redis import RedisCacheBackend
from app.core.config import settings
from sqlalchemy import select, delete

cache = RedisCacheBackend(settings.REDIS_URL, settings.CACHE_TTL_SECONDS)

async def get_all_posts_crud(session: AsyncSession, user_id: int):
    cached_posts = cache.get(settings.POST_CACHED_KEY)
    if cached_posts:
        return cached_posts
    
    stmt = select(Post).where(Post.user_id == user_id)
    result = await session.execute(stmt)
    posts = result.scalars().all()
    posts_read = [PostSchema.model_validate(post) for post in posts]
    post_for_cache = [post.model_dump() for post in posts_read]
    cache.set(settings.POST_CACHED_KEY, post_for_cache)
    
    return posts


async def create_post_crud(session: AsyncSession, post: PostSchema, user_id: int):
    cache.delete(settings.POST_CACHED_KEY)
    new_post = Post(**post.model_dump(), user_id=user_id)
    session.add(new_post)
    await session.commit()
    await session.refresh(new_post)
    return new_post


async def delete_all_posts(session: AsyncSession,user_id: int):
    cache.delete(settings.POST_CACHED_KEY)
    stmt = delete(Post).where(Post.user_id == user_id)
    await session.execute(stmt)
    await session.commit()
    return {"message": "Посты были удалены"}