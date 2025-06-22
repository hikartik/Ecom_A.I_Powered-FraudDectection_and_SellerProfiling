import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def trigger_all_updates():
    """Trigger the manual all updates endpoint"""
    print("Triggering manual update for all scores...")
    print("This will update both review scores and seller scores.")
    
    try:
        response = requests.post(f"{BASE_URL}/admin/trigger-all-updates")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ All updates successfully triggered. Server response:")
            print(json.dumps(data, indent=2))
        else:
            print(f"❌ Failed to trigger all updates. Status code: {response.status_code}")
            print(f"Response body: {response.text}")
            
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection Error: Could not connect to the server at {BASE_URL}.")
        print("Please ensure the backend server is running.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

def check_server_readiness():
    """Check if the server is ready to accept connections."""
    print("Waiting for the server to be ready...")
    for _ in range(10): # Try for 10 seconds
        try:
            response = requests.get(BASE_URL)
            if response.status_code == 200:
                print("✅ Server is ready.")
                return True
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(1)
    print("❌ Server did not become ready in time.")
    return False

if __name__ == "__main__":
    if check_server_readiness():
        trigger_all_updates() 