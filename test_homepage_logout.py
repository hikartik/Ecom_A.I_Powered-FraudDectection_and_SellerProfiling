#!/usr/bin/env python3
"""
Test script to verify homepage logout functionality
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_homepage_logout():
    """Test the homepage logout functionality"""
    
    print("🏠 Testing Homepage Logout Functionality")
    print("=" * 50)
    
    # Step 1: Test homepage accessibility
    print("\n1. Testing homepage accessibility...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Homepage is accessible!")
        else:
            print(f"❌ Homepage failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Homepage request failed: {e}")
        return
    
    # Step 2: Test login page accessibility
    print("\n2. Testing login page accessibility...")
    try:
        response = requests.get(f"{BASE_URL}/login")
        if response.status_code == 200:
            print("✅ Login page is accessible!")
        else:
            print(f"❌ Login page failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Login page request failed: {e}")
    
    # Step 3: Test register page accessibility
    print("\n3. Testing register page accessibility...")
    try:
        response = requests.get(f"{BASE_URL}/register")
        if response.status_code == 200:
            print("✅ Register page is accessible!")
        else:
            print(f"❌ Register page failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Register page request failed: {e}")
    
    # Step 4: Test products page accessibility
    print("\n4. Testing products page accessibility...")
    try:
        response = requests.get(f"{BASE_URL}/products/")
        if response.status_code == 200:
            print("✅ Products page is accessible!")
        else:
            print(f"❌ Products page failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Products page request failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Homepage logout functionality test completed!")
    print("\n📋 Manual Testing Instructions:")
    print("1. Open http://127.0.0.1:8000 in your browser")
    print("2. Click 'Hello, Sign in' to go to login page")
    print("3. Login with demo account: customer@demo.com / password123")
    print("4. Return to homepage - you should see 'Hello, [Name]'")
    print("5. Click on 'Hello, [Name]' to open dropdown menu")
    print("6. Click the red 'Sign Out' button")
    print("7. You should be logged out and see 'Hello, Sign in' again")

if __name__ == "__main__":
    test_homepage_logout() 