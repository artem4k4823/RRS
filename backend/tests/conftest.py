from sqlalchemy import true
import pytest
# pyrefly: ignore [missing-import]
from main import app
from fastapi.testclient import  TestClient

@pytest.fixture
def test_client():
    return TestClient(app)

@pytest.fixture(autouse= True)
def clears_posts():
    tasks.clear()