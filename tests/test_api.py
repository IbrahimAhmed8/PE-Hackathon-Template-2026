import pytest
from app import create_app
from app.database import db
from app.models.product import Product

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.app_context():
        db.create_tables([Product])
        yield app.test_client()
        db.drop_tables([Product])

def test_health_check(client):
    res = client.get("/health")
    assert res.status_code == 200

def test_create_and_get_product(client):
    res = client.post("/products", json={"name": "Laptop", "price": 1000.50, "stock": 10})
    assert res.status_code == 201
    res_get = client.get("/products")
    assert len(res_get.json) == 1

def test_bad_input(client):
    res = client.post("/products", json={"name": "Mouse"})
    assert res.status_code == 400

def test_uniqueness(client):
    client.post("/products", json={"name": "Keyboard", "price": 50})
    res = client.post("/products", json={"name": "Keyboard", "price": 60})
    assert res.status_code == 409

def test_not_found(client):
    res = client.get("/products/999")
    assert res.status_code == 404
