import requests
import json

# Test admin login and API access
BASE_URL = "http://localhost:8000"

def test_admin_auth():
    # Login as admin2
    login_data = {
        "email": "admin2@example.com",
        "password": "12345678"
    }
    
    print("Testing admin2 login...")
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"Login response status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        token = data.get("access_token")
        user_type = data.get("user_type")
        user_id = data.get("user_id")
        
        print(f"Login successful!")
        print(f"User type: {user_type}")
        print(f"User ID: {user_id}")
        print(f"Token: {token[:50]}...")
        
        # Test admin products endpoint
        headers = {"Authorization": f"Bearer {token}"}
        print("\nTesting admin products endpoint...")
        products_response = requests.get(f"{BASE_URL}/admin/products", headers=headers)
        print(f"Products response status: {products_response.status_code}")
        
        if products_response.status_code == 200:
            products = products_response.json()
            print(f"Found {len(products)} products")
            for product in products[:3]:  # Show first 3 products
                print(f"- {product.get('product_name', 'N/A')} (ID: {product.get('id', 'N/A')})")
        else:
            print(f"Error response: {products_response.text}")
    else:
        print(f"Login failed: {response.text}")

if __name__ == "__main__":
    test_admin_auth() 