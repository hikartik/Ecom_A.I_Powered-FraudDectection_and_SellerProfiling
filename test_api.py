#!/usr/bin/env python3
"""
Test script to check the API response
"""

import requests
import json

def test_api():
    try:
        response = requests.get("http://localhost:8000/products/api/")
        if response.status_code == 200:
            products = response.json()
            print(f"Found {len(products)} products:")
            for i, product in enumerate(products):
                print(f"\nProduct {i+1}:")
                print(f"  Name: {product.get('product_name', 'N/A')}")
                print(f"  Description: {product.get('description', 'N/A')}")
                print(f"  Status: {product.get('status', 'N/A')}")
                print(f"  Ensemble Score: {product.get('ensemble_score', 'N/A')}")
                print(f"  Vision Score: {product.get('vision_score', 'N/A')}")
                print(f"  Text Score: {product.get('text_score', 'N/A')}")
                print(f"  Risk Label: {product.get('risk_label', 'N/A')}")
        else:
            print(f"API returned status code: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api() 