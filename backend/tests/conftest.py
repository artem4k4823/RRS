import sys
from pathlib import Path

backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

import pytest
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.pool import NullPool
from app.core.models import User
from app.core.models.base import Base
from main import app
from app.core.database import db as get_db
from app.auth.token import create_access_token
from app.auth.auth_helper import hash_password


TEST_DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5435/test_db"


@pytest.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    yield engine
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture(scope="function")
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    connection = await test_engine.connect()
    transaction = await connection.begin()

    session = AsyncSession(
        bind=connection,
        expire_on_commit=False,
        join_transaction_mode="create_savepoint"
    )

    yield session

    await session.close()
    await transaction.rollback()
    await connection.close()


@pytest.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[get_db.session_getter] = lambda: db_session

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
async def test_user(db_session: AsyncSession) -> User:
    """Фикстура для создания обычного тестового пользователя."""
    user = User(
        username="test_user",
        password=hash_password("testpassword123"),
        status=True,
        isAdmin=False,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
async def auth_client(client: AsyncClient, test_user: User) -> AsyncClient:
    """Фикстура HTTP-клиента с автоматически прикрепленным Bearer-токеном авторизации."""
    access_token = await create_access_token(user_id=test_user.id)
    client.headers.update({"Authorization": f"Bearer {access_token}"})
    return client


@pytest.fixture(scope="function")
async def admin_user(db_session: AsyncSession) -> User:
    """Фикстура для создания тестового пользователя-администратора."""
    user = User(
        username="admin_user",
        password=hash_password("adminpassword123"),
        status=True,
        isAdmin=True,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture(scope="function")
async def admin_auth_client(client: AsyncClient, admin_user: User) -> AsyncClient:
    """Фикстура HTTP-клиента с Bearer-токеном пользователя-администратора."""
    access_token = await create_access_token(user_id=admin_user.id)
    client.headers.update({"Authorization": f"Bearer {access_token}"})
    return client