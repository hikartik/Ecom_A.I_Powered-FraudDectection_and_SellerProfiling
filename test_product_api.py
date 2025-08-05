import requests
import pytest
import json

# Test product API endpoints
BASE_URL = "http://localhost:8000"

def test_product_api():
    try:
        response = requests.get(f"{BASE_URL}/products/api/", timeout=0.5)
    except requests.exceptions.RequestException:
        pytest.skip("API server not available")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

if __name__ == "__main__":
    test_product_api() 