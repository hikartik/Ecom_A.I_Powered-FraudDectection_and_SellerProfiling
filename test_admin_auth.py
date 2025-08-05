import requests
import pytest
import json

# Test admin login and API access
BASE_URL = "http://localhost:8000"

def test_admin_auth():
    login_data = {"email": "admin2@example.com", "password": "12345678"}
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data, timeout=0.5)
    except requests.exceptions.RequestException:
        pytest.skip("API server not available")

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

if __name__ == "__main__":
    test_admin_auth() 