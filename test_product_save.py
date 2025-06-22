import requests
import json

# Test product save functionality
BASE_URL = "http://localhost:8000"

def test_product_save():
    print("Testing product save functionality...")
    
    # First, login as a seller to get a token
    login_data = {
        "email": "seller1@example.com",
        "password": "seller123"
    }
    
    print("\n1. Testing seller login...")
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"Login response status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        token = data.get("access_token")
        print(f"Login successful! Token: {token[:50]}...")
        
        # Test product save endpoint
        print("\n2. Testing product save endpoint...")
        
        # Create a simple product without image for testing
        product_data = {
            "product_name": "Test Product",
            "description": "This is a test product",
            "price": 99.99
        }
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test with form data (simulating file upload)
        from requests_toolbelt import MultipartEncoder
        
        try:
            m = MultipartEncoder(
                fields={
                    'product_name': 'Test Product',
                    'description': 'This is a test product',
                    'price': '99.99'
                }
            )
            
            headers['Content-Type'] = m.content_type
            
            response = requests.post(
                f"{BASE_URL}/products/add",
                data=m,
                headers=headers
            )
            
            print(f"Product save response status: {response.status_code}")
            print(f"Response text: {response.text}")
            
            if response.status_code == 200:
                print("Product saved successfully!")
            else:
                print("Failed to save product")
                
        except ImportError:
            print("requests_toolbelt not available, testing with JSON...")
            
            # Fallback to JSON test
            response = requests.post(
                f"{BASE_URL}/products/add",
                json=product_data,
                headers=headers
            )
            
            print(f"Product save response status: {response.status_code}")
            print(f"Response text: {response.text}")
            
    else:
        print(f"Login failed: {response.text}")

if __name__ == "__main__":
    test_product_save() 