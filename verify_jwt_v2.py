import requests
import json
import uuid
import sys
import time

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True)

BASE_URL = "http://localhost:8000"
session = requests.Session()

def test_jwt_flow():
    print("--- START JWT VERIFICATION ---")
    
    # 1. Signup
    short_uuid = str(uuid.uuid4())[:8]
    email = f"jwt_user_{short_uuid}@example.com"
    password = "password123"
    
    print(f"1. Signing up user: {email}")
    payload = {
        "name": "JWT User",
        "email": email,
        "password": password,
        "role": "tester"
    }
    
    try:
        response = session.post(f"{BASE_URL}/auth/signup", json=payload)
        print(f"   Status: {response.status_code}")
        if response.status_code != 200:
            print(f"   Signup failed: {response.text}")
            return
        
        # 2. Login
        print("2. Logging in...")
        login_payload = {"email": email, "password": password}
        response = session.post(f"{BASE_URL}/auth/login", json=login_payload)
        print(f"   Status: {response.status_code}")
        
        if response.status_code != 200:
             print(f"   Login failed: {response.text}")
             return
             
        data = response.json()
        access_token = data.get("access_token")
        if access_token:
            print("   Access Token received.")
        else:
            print("   No access token received!")

        # 3. Access Protected Route (/me)
        print("3. Accessing protected route (/auth/me)...")
        headers = {"Authorization": f"Bearer {access_token}"}
        response = session.get(f"{BASE_URL}/auth/me", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Success! User: {response.json().get('email')}")
        else:
            print(f"   Failed: {response.text}")

        # 4. Refresh Token
        print("4. Refreshing token (using cookie)...")
        # Ensure cookie is sent
        response = session.post(f"{BASE_URL}/auth/refresh")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            new_access_token = response.json().get("access_token")
            print("   New Access Token received.")
        else:
            print(f"   Refresh failed: {response.text}")

        # 5. Logout
        print("5. Logging out...")
        response = session.post(f"{BASE_URL}/auth/logout")
        print(f"   Status: {response.status_code}")
        
        # Verify refresh fails
        print("   Verifying refresh fails after logout...")
        response = session.post(f"{BASE_URL}/auth/refresh")
        print(f"   Status: {response.status_code}")
        if response.status_code == 401:
            print("   Correct: Refresh rejected.")
        else:
            print(f"   Incorrect: Expected 401, got {response.status_code}")

    except Exception as e:
        print(f"Exception: {e}")
    finally:
        print("--- END JWT VERIFICATION ---")

if __name__ == "__main__":
    test_jwt_flow()
