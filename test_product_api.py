import requests
import json

# Test product API endpoints
BASE_URL = "http://localhost:8000"

def test_product_api():
    print("Testing product API endpoints...")
    
    # Test getting all products
    print("\n1. Testing GET /products/api/")
    response = requests.get(f"{BASE_URL}/products/api/")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        products = response.json()
        print(f"Found {len(products)} products")
        
        if len(products) > 0:
            first_product = products[0]
            print(f"First product:")
            print(f"  ID: {first_product.get('id', 'MISSING')}")
            print(f"  _id: {first_product.get('_id', 'MISSING')}")
            print(f"  Name: {first_product.get('product_name', 'MISSING')}")
            print(f"  Status: {first_product.get('status', 'MISSING')}")
            
            # Test getting single product
            product_id = first_product.get('id') or first_product.get('_id')
            if product_id:
                print(f"\n2. Testing GET /products/api/{product_id}")
                single_response = requests.get(f"{BASE_URL}/products/api/{product_id}")
                print(f"Status: {single_response.status_code}")
                
                if single_response.status_code == 200:
                    product = single_response.json()
                    print(f"Single product:")
                    print(f"  ID: {product.get('id', 'MISSING')}")
                    print(f"  Name: {product.get('product_name', 'MISSING')}")
                    print(f"  Status: {product.get('status', 'MISSING')}")
                else:
                    print(f"Error: {single_response.text}")
            else:
                print("No product ID found to test single product endpoint")
        else:
            print("No products found")
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    test_product_api() 