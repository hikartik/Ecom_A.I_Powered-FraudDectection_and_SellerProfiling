import requests
import json

# Test JWT token
def test_jwt_token():
    token = "eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJ1c2VyX2lkIjogIjY4NTdkODM1YmMxZGI4OTZiZmQwMTE1NSIsICJleHAiOiAiMjAyNS0wNi0yMlQxMTo0Mzo0OS4wNjUzODAifQ.NmE1MjU4OTViMWQ5NDEyYjI5OGIwMjkyYmQyZmEzNjA2MDJlOTNiMGQ5NTllZDU0ZjdjZjA3YTQ5ZjFjZmVhNQ"
    
    # Test if token is valid by calling a protected endpoint
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json'
    }
    
    try:
        # Test with a simple endpoint first
        response = requests.get('http://localhost:8000/products/my', headers=headers)
        print(f"JWT Test Status: {response.status_code}")
        print(f"JWT Test Response: {response.text}")
        
        if response.status_code == 200:
            print("JWT token is valid!")
            return True
        else:
            print("JWT token is invalid!")
            return False
            
    except Exception as e:
        print(f"JWT Test Error: {e}")
        return False

# Test product addition
def test_add_product():
    token = "eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJ1c2VyX2lkIjogIjY4NTdkODM1YmMxZGI4OTZiZmQwMTE1NSIsICJleHAiOiAiMjAyNS0wNi0yMlQxMTo0Mzo0OS4wNjUzODAifQ.NmE1MjU4OTViMWQ5NDEyYjI5OGIwMjkyYmQyZmEzNjA2MDJlOTNiMGQ5NTllZDU0ZjdjZjA3YTQ5ZjFjZmVhNQ"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json'
    }
    
    # Create a simple test image (1x1 pixel)
    test_image_data = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\x08\x06\x06\x07\x06\x05\x08\x07\x07\x07\t\t\x08\n\x0c\x14\r\x0c\x0b\x0b\x0c\x19\x12\x13\x0f\x14\x1d\x1a\x1f\x1e\x1d\x1a\x1c\x1c $.\' ",#\x1c\x1c(7),01444\x1f\'9=82<.342\xff\xc0\x00\x11\x08\x00\x01\x00\x01\x01\x01\x11\x00\x02\x11\x01\x03\x11\x01\xff\xc4\x00\x14\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\xff\xc4\x00\x14\x10\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xda\x00\x0c\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00\xaa\xff\xd9'
    
    files = {
        'images': ('test.jpg', test_image_data, 'image/jpeg')
    }
    
    data = {
        'product_name': 'Test Product',
        'description': 'Test Description'
    }
    
    try:
        response = requests.post(
            'http://localhost:8000/products/add',
            headers=headers,
            files=files,
            data=data
        )
        print(f"Add Product Status: {response.status_code}")
        print(f"Add Product Response: {response.text}")
        
    except Exception as e:
        print(f"Add Product Error: {e}")

if __name__ == "__main__":
    print("Testing JWT token...")
    if test_jwt_token():
        print("\nTesting product addition...")
        test_add_product()
    else:
        print("JWT token is invalid, cannot test product addition") 