#!/usr/bin/env python3
"""
Test script to verify logout functionality
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_logout_flow():
    """Test the complete login and logout flow"""
    
    print("🧪 Testing Logout Functionality")
    print("=" * 50)
    
    # Step 1: Login with demo user
    print("\n1. Logging in with demo customer...")
    login_data = {
        "email": "customer@demo.com",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            token = response.json().get("access_token")
            print(f"✅ Login successful! Token received: {token[:20]}...")
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"❌ Login request failed: {e}")
        return
    
    # Step 2: Test accessing protected endpoint
    print("\n2. Testing access to protected endpoint...")
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        if response.status_code == 200:
            user_info = response.json()
            print(f"✅ Protected endpoint accessible! User: {user_info.get('full_name')}")
        else:
            print(f"❌ Protected endpoint failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Protected endpoint request failed: {e}")
    
    # Step 3: Test logout endpoint
    print("\n3. Testing logout endpoint...")
    try:
        response = requests.post(f"{BASE_URL}/auth/logout", headers=headers)
        if response.status_code == 200:
            print("✅ Logout endpoint successful!")
        else:
            print(f"❌ Logout endpoint failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Logout request failed: {e}")
    
    # Step 4: Test that token is no longer valid
    print("\n4. Testing that token is invalid after logout...")
    try:
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        if response.status_code == 401:
            print("✅ Token correctly invalidated after logout!")
        else:
            print(f"⚠️  Token still valid after logout: {response.status_code}")
    except Exception as e:
        print(f"❌ Token validation request failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Logout functionality test completed!")

if __name__ == "__main__":
    test_logout_flow() 