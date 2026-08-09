from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.models.favorite_url import FavoriteUrl
from app.core.models.rss_list import OptionalUrl
from app.core.models.subscribtion import Subscription
from fastapi import HTTPException, status
from sqlalchemy import select



async def add_to_favorite(session: AsyncSession, user_id: int, url_id: int):
    stmt = select(OptionalUrl).where(OptionalUrl.id == url_id)
    res = await session.execute(stmt)
    optional_url = res.scalar_one_or_none()
    
    if not optional_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Ссылка не найдена"
        )
    
    fav_stmt = select(FavoriteUrl).where(
        FavoriteUrl.user_id == user_id,
        FavoriteUrl.url_id == url_id
    )
    existing_fav = (await session.execute(fav_stmt)).scalar_one_or_none()
    if existing_fav:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Ссылка уже в избранном"
        )
        
    new_favorite_url = FavoriteUrl(
        user_id=user_id,
        url_id=url_id
    )

    optional_url.likes += 1
    session.add(new_favorite_url)
    await session.commit()
    return {"message":"Успешно добавлено в избранное"}


async def delete_from_favorites(session: AsyncSession, url_id: int, user_id: int):
    stmt = select(FavoriteUrl).where(
        FavoriteUrl.user_id == user_id,
        FavoriteUrl.url_id == url_id
    )
    res = await session.execute(stmt)
    favorite = res.scalar_one_or_none()

    if not favorite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ссылка не найдена в избранном"
        )

    url_stmt = select(OptionalUrl).where(OptionalUrl.id == url_id)
    url_res = await session.execute(url_stmt)
    optional_url = url_res.scalar_one_or_none()

    if optional_url and optional_url.likes > 0:
        optional_url.likes -= 1

    await session.delete(favorite)
    await session.commit()
    return {"detail": "Удалено из избранного"}


async def get_all_user_favorite_urls(session: AsyncSession, user_id: int):
    stmt = select(FavoriteUrl).options(joinedload(FavoriteUrl.optional_url)).where(FavoriteUrl.user_id == user_id)
    res = await session.execute(stmt)
    result = res.scalars().all()
    return result