from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_password():
    response = client.post("/password/test_service", json={"password": "mypassword"})
    assert response.status_code == 200
    assert response.json()["service_name"] == "test_service"


def test_get_password():
    response = client.get("/password/test_service")
    assert response.status_code == 200
    assert response.json()["password"] == "mypassword"


def test_search_passwords():
    response = client.get("/password/?service_name=test")
    assert response.status_code == 200
    assert "test_service" in response.json()
