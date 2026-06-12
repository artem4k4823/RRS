from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.post import PostSchema
from app.core.models.post import Post
from app.schemas.post import PostSchema
from app.cache.redis import RedisCacheBackend
from app.core.config import settings
from sqlalchemy import select

cache = RedisCacheBackend(settings.REDIS_URL, settings.CACHE_TTL_SECONDS)

async def get_all_posts_crud(session: AsyncSession):
    cached_posts = cache.get(settings.POST_CACHED_KEY)
    if cached_posts:
        return cached_posts
    
    stmt = select(Post)
    result = await session.execute(stmt)
    posts = result.scalars().all()
    posts_read = [PostSchema.model_validate(post) for post in posts]
    post_for_cache = [post.model_dump() for post in posts_read]
    cache.set(settings.POST_CACHED_KEY, post_for_cache)
    
    return posts


async def create_post_crud(session: AsyncSession, post: PostSchema):
    cache.delete(settings.POST_CACHED_KEY)
    new_post = Post(
        title = post.title,
        description = post.description,
        text = post.text,
    )
    session.add(new_post)
    await session.commit()
    return 'Пост создан успешно'