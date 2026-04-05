import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    yield app.test_client()

def test_health_check(client):
    res = client.get("/health")
    assert res.status_code == 200