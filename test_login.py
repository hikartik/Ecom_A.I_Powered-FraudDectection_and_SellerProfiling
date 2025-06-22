import requests
import json

# Test login endpoint
def test_login():
    url = "http://localhost:8000/users/login"
    data = {
        "email": "seller2@example.com",
        "password": "123@"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print("Login successful!")
            print(f"Token: {result.get('token', 'No token')}")
            print(f"User: {result.get('user', 'No user data')}")
        else:
            print("Login failed!")
            
    except Exception as e:
        print(f"Error: {e}")

# Test register endpoint first
def test_register():
    url = "http://localhost:8000/users/register"
    data = {
        "name": "Test Seller",
        "email": "seller2@example.com",
        "password": "123@",
        "type": "seller"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Register Status Code: {response.status_code}")
        print(f"Register Response: {response.text}")
        
        if response.status_code == 201:
            print("Registration successful!")
        else:
            print("Registration failed or user already exists!")
            
    except Exception as e:
        print(f"Register Error: {e}")

if __name__ == "__main__":
    print("Testing registration...")
    test_register()
    print("\nTesting login...")
    test_login() 