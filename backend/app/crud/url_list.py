from app.schemas import oprional_url
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.core.models.rss_list import OptionalUrl
from app.schemas.oprional_url import OptionalUrlSchema

async def add_optional_url(session: AsyncSession, optional_url: OptionalUrlSchema):
    new_url =OptionalUrl(
        name = optional_url.name,
        description = optional_url.description,
        url = optional_url.url
    )
    
    session.add(new_url)
    await session.commit()

async def get_all_optional_url(session: AsyncSession):
    stmt = select(OptionalUrl)
    res = await session.execute(stmt)
    result = res.scalars().all()
    return result

async def delete_optional_url(session: AsyncSession, url_id):
    stmt = delete(OptionalUrl).where(OptionalUrl.id == url_id)
    await session.execute(stmt)
    await session.commit()

