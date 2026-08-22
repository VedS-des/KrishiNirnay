import json
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/")
    print("1. [GET /] Status:", response.status_code)
    print("   Response:", response.json())
    assert response.status_code == 200
    assert response.json() == {"message": "KrishiNirnay Backend is running!"}


def test_farms_endpoint():
    payload = {
        "location": "Tamil Nadu",
        "latitude": 11.0168,
        "longitude": 76.9558,
        "area": 5.0,
        "soil_type": "red",
        "soil_ph": 6.8,
        "water_availability": "medium",
        "budget": 150000.0,
        "season": "kharif",
        "previous_crop": "groundnut",
    }
    response = client.post("/farms", json=payload)
    print("\n2. [POST /farms] Status:", response.status_code)
    print("   Response:", json.dumps(response.json(), indent=2))
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Farm details received successfully"
    assert data["farm"]["location"] == "Tamil Nadu"
    assert data["farm"]["budget"] == 150000.0


def test_recommend_endpoint():
    payload = {
        "location": "Tamil Nadu",
        "latitude": 11.0168,
        "longitude": 76.9558,
        "area": 5.0,
        "soil_type": "red",
        "soil_ph": 6.8,
        "water_availability": "medium",
        "budget": 150000.0,
        "season": "kharif",
        "previous_crop": "groundnut",
    }
    response = client.post("/recommend", json=payload)
    print("\n3. [POST /recommend] Status:", response.status_code)
    print("   Response:", json.dumps(response.json(), indent=2))
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data
    assert len(data["recommendations"]) == 3
    assert data["recommendations"][0]["crop"] == "Groundnut"
    assert data["recommendations"][0]["score"] == 91
    assert data["recommendations"][0]["risk"] == "Low"


def test_docs_and_openapi():
    response = client.get("/openapi.json")
    print("\n4. [GET /openapi.json] Status:", response.status_code)
    assert response.status_code == 200
    paths = response.json()["paths"]
    print("   Registered OpenAPI Paths:", list(paths.keys()))
    assert "/" in paths
    assert "/farms" in paths
    assert "/recommend" in paths

    docs_response = client.get("/docs")
    print("\n5. [GET /docs] Status:", docs_response.status_code)
    assert docs_response.status_code == 200


if __name__ == "__main__":
    print("Starting KrishiNirnay Backend Automated Tests...\n")
    test_health_check()
    test_farms_endpoint()
    test_recommend_endpoint()
    test_docs_and_openapi()
    print("\n==========================================")
    print("ALL TESTS PASSED SUCCESSFULLY (5/5)!")
    print("==========================================")
