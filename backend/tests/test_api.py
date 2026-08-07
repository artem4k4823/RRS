import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.models import User


async def test_get_health(client: AsyncClient):
    """Тест эндпоинта проверки работоспособности сервера (/health)."""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_get_root(client: AsyncClient):
    """Тест корневого эндпоинта (/), возвращающего HTML."""
    response = await client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")


async def test_register_user_success(client: AsyncClient, db_session: AsyncSession):
    """Тест успешной регистрации нового пользователя с использованием тестовой БД."""
    payload = {
        "username": "testuser_unauth",
        "password": "strongpassword123",
    }
    response = await client.post("/api/user/register_user", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["username"] == "testuser_unauth"
    assert "id" in data

    result = await db_session.execute(
        select(User).where(User.username == "testuser_unauth")
    )
    user_in_db = result.scalar_one_or_none()
    assert user_in_db is not None
    assert user_in_db.username == "testuser_unauth"


async def test_register_user_validation_error(client: AsyncClient):
    """Тест валидации данных при отсутствии обязательного поля password (422 Unprocessable Entity)."""
    payload = {
        "username": "invaliduser",
    }
    response = await client.post("/api/user/register_user", json=payload)
    assert response.status_code == 422


async def test_send_url_for_generate_rss_success(client: AsyncClient):
    """Тест генерации ссылки RSS для корректного URL."""
    payload = {"url": "https://example.com", "pages": 1}
    response = await client.post("/generate-rrs-from-url/send-url-for-generate-rss", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "rss_link" in data
    assert "feed" in data["rss_link"]


async def test_send_url_for_generate_rss_invalid_url(client: AsyncClient):
    """Тест отправки невалидного URL для генерации RSS (400 Bad Request)."""
    payload = {"url": "not_a_valid_url", "pages": 1}
    response = await client.post("/generate-rrs-from-url/send-url-for-generate-rss", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Не подходящий URL"


async def test_get_optonal_url_list(auth_client: AsyncClient):
    """Тест получения списка опциональных ссылок на RSS ленты авторизованным пользователем."""
    response = await auth_client.get("/optional_url_list/get-all-optionals-urls")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_get_me_authorized(auth_client: AsyncClient, test_user: User):
    """Тест получения данных текущего авторизованного пользователя (/auth/me)."""
    response = await auth_client.get("/auth/me")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_user.id
    assert data["username"] == test_user.username

async def test_add_url_to_sub(auth_client: AsyncClient):
    """тест на добавление ссылки в избранное где ссылка валидна"""
    payload = {"url":"https://www.jagonews24.com/rss/rss.xml","custom_name":"test"}
    response = await auth_client.post("/subscriptions/add-subs", json=payload)
    assert response.status_code == 200

async def test_add_url_to_sub_invalid_url(auth_client: AsyncClient):
    """тест на добавление ссылки в избранное где ссылка не валидна"""
    payload = {"url":"test","custom_name":"test"}
    response = await auth_client.post("/subscriptions/add-subs", json=payload)
    assert response.status_code == 400
    

async def test_get_all_subs(auth_client: AsyncClient):
    """ Тест получения данных всех подписок пользователя"""
    respone = await auth_client.get("/subscriptions/get-all-subs")
    assert respone.status_code == 200
    data = respone.json()
    if len(data)> 0:
        assert isinstance(data[0]["feed_url"], str)
    