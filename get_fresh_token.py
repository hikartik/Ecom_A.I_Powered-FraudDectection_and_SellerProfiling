import requests
import json

def get_fresh_token():
    """Get a fresh JWT token by logging in"""
    
    # First, register a user if they don't exist
    register_data = {
        "name": "Test Seller",
        "email": "seller2@example.com",
        "password": "123@",
        "type": "seller"
    }
    
    try:
        # Try to register
        register_response = requests.post(
            "http://localhost:8000/users/register",
            json=register_data
        )
        print(f"Register status: {register_response.status_code}")
        if register_response.status_code == 201:
            print("User registered successfully")
        else:
            print("User might already exist")
    except Exception as e:
        print(f"Register error: {e}")
    
    # Now login to get a fresh token
    login_data = {
        "email": "seller2@example.com",
        "password": "123@"
    }
    
    try:
        login_response = requests.post(
            "http://localhost:8000/users/login",
            json=login_data
        )
        
        print(f"Login status: {login_response.status_code}")
        print(f"Login response: {login_response.text}")
        
        if login_response.status_code == 200:
            result = login_response.json()
            token = result.get('token')
            print(f"\n✅ Fresh JWT Token: {token}")
            print(f"\nUse this curl command:")
            print(f"curl -X 'POST' \\")
            print(f"  'http://localhost:8000/products/add' \\")
            print(f"  -H 'accept: application/json' \\")
            print(f"  -H 'Authorization: Bearer {token}' \\")
            print(f"  -H 'Content-Type: multipart/form-data' \\")
            print(f"  -F 'product_name=Samsung Galaxy A13' \\")
            print(f"  -F 'description=Smartphone best ever' \\")
            print(f"  -F 'images=@81H6vveSIZL.jpg;type=image/jpeg'")
            return token
        else:
            print("❌ Login failed!")
            return None
            
    except Exception as e:
        print(f"Login error: {e}")
        return None

if __name__ == "__main__":
    get_fresh_token() 