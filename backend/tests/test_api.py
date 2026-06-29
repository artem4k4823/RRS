from fastapi.testclient import TestClient
# pyrefly: ignore [missing-import]
from main import app


def test_get_health(test_client: TestClient):
    response = test_client.get('/health')
    
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}