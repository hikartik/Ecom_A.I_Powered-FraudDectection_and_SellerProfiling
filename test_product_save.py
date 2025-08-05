import requests
import pytest
import json

# Test product save functionality
BASE_URL = "http://localhost:8000"

def test_product_save():
    login_data = {"email": "seller1@example.com", "password": "seller123"}
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data, timeout=0.5)
    except requests.exceptions.RequestException:
        pytest.skip("API server not available")

    assert response.status_code == 200
    data = response.json()
    token = data.get("access_token")
    assert token

    headers = {"Authorization": f"Bearer {token}"}
    product_data = {
        "product_name": "Test Product",
        "description": "This is a test product",
        "price": 99.99,
    }

    try:
        from requests_toolbelt import MultipartEncoder

        m = MultipartEncoder(
            fields={
                "product_name": "Test Product",
                "description": "This is a test product",
                "price": "99.99",
            }
        )
        headers["Content-Type"] = m.content_type
        save_resp = requests.post(f"{BASE_URL}/products/add", data=m, headers=headers, timeout=0.5)
    except Exception:
        save_resp = requests.post(
            f"{BASE_URL}/products/add", json=product_data, headers=headers, timeout=0.5
        )

    assert save_resp.status_code in {200, 201}

if __name__ == "__main__":
    test_product_save() 