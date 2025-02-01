import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.utils.test_auth import TestAuth

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def auth_headers():
    return TestAuth.get_test_token()