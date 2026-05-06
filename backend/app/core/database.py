from sqlalchemy.ext.asyncio import async_session, async_sessionmaker, create_async_engine,
from core.config import settings


class Database:
    def __init__(self, url: str):
        self.engine = create_async_engine(
            url = url
        )
        
        self.session_maker = async_sessionmaker(
            bind=False,
            autoflush=False,
            autocommit = False,
            expire_on_commit=False,
        )
        
    async def session_getter(self):
        async with self.session_maker as session:
            yield session
            await session.commit()
                
db = Database(url=settings.database.database_url)