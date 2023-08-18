from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200

def test_read_health():
    response = client.get("/health")
    assert response.status_code == 200

def test_read_health_kubernetes():
    response = client.get("/health/kubernetes")
    assert response.status_code == 200

def test_authentication():
    response = client.post("/process")
    assert response.status_code == 401.