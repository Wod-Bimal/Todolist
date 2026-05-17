from fastapi.testclient import TestClient
from app import app  # Import your FastAPI app object

# Create the TestClient instance
client = TestClient(app)

# Test 1: Testing a basic GET request
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

# Test 2: Testing a POST request with JSON data
def test_create_item():
    response = client.post("/items/", json={"name": "Laptop"})
    assert response.status_code == 200
    assert response.json() == {"message": "Created Laptop"}

# Test 3: Testing error/invalid data validation
def test_create_item_invalid():
    # Sending an empty dictionary instead of {"name": "..."}
    response = client.post("/items/", json={})
    assert response.status_code == 422  # 422 is FastAPI's validation error code
