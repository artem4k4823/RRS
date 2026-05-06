from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.post import PostSchema
from app.core.models.post import Post
from sqlalchemy import select


async def get_all_posts_crud(session: AsyncSession):
    stmt = select(Post)
    result = await session.execute(stmt)
    posts = result.scalars().all()
    return posts


async def create_post_crud(session: AsyncSession, post: PostSchema):
    new_post = Post(
        title = post.title,
        description = post.description,
        text = post.text,
    )
    session.add(new_post)
    await session.commit()
    return 'Пост создан успешно'