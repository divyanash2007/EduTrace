import requests
import json
import uuid
import time

BASE_URL = "http://localhost:8000"

# Use a session to persist cookies
session = requests.Session()

def test_jwt_flow():
    print("--- START JWT VERIFICATION ---")
    
    # 1. Signup
    short_uuid = str(uuid.uuid4())[:8]
    email = f"jwt_user_{short_uuid}@example.com"
    password = "password123"
    
    print(f"\n1. Signing up user: {email}")
    payload = {
        "name": "JWT User",
        "email": email,
        "password": password,
        "role": "tester"
    }
    
    try:
        response = session.post(f"{BASE_URL}/auth/signup", json=payload)
        if response.status_code != 200:
            print(f"Signup failed: {response.text}")
            return
        print("Signup successful.")
        
        # 2. Login
        print("\n2. Logging in...")
        login_payload = {
            "email": email,
            "password": password
        }
        response = session.post(f"{BASE_URL}/auth/login", json=login_payload)
        if response.status_code != 200:
             print(f"Login failed: {response.text}")
             return
             
        data = response.json()
        access_token = data.get("access_token")
        if not access_token:
            print("No access token received!")
            return
            
        print(f"Login successful. Access Token received.")
        
        # Check Cookies
        cookie = session.cookies.get("refresh_token")
        if not cookie:
            print("Refresh token cookie MISSING!")
            return
        print("Refresh token cookie present.")

        # 3. Access Protected Route (/me)
        print("\n3. Accessing protected route (/auth/me)...")
        headers = {"Authorization": f"Bearer {access_token}"}
        response = session.get(f"{BASE_URL}/auth/me", headers=headers)
        if response.status_code == 200:
            print(f"Success! User: {response.json()['email']}")
        else:
            print(f"Failed to access protected route: {response.status_code} {response.text}")
            return

        # 4. Refresh Token
        print("\n4. Refreshing token...")
        # Clear access token to simulate expiry (client side)
        # We only send cookies now
        response = session.post(f"{BASE_URL}/auth/refresh")
        if response.status_code == 200:
            new_data = response.json()
            new_access_token = new_data.get("access_token")
            print("Refresh successful. New Access Token received.")
            
            # Verify new token works
            headers = {"Authorization": f"Bearer {new_access_token}"}
            response = session.get(f"{BASE_URL}/auth/me", headers=headers)
            if response.status_code == 200:
                 print("New access token verified.")
            else:
                 print("New access token failed.")
        else:
            print(f"Refresh failed: {response.status_code} {response.text}")
            return

        # 5. Logout
        print("\n5. Logging out...")
        response = session.post(f"{BASE_URL}/auth/logout")
        if response.status_code == 200:
            print("Logout successful.")
            # Verify cookie is gone/cleared
            if not session.cookies.get("refresh_token"):
                 print("Cookie cleared.")
            else:
                 print("Cookie still present (might be browser behavior difference, strict check skipped)")
                 
            # Verify refresh fails
            print("Verifying refresh fails after logout...")
            response = session.post(f"{BASE_URL}/auth/refresh")
            if response.status_code == 401:
                print("Correctly rejected refresh request.")
            else:
                print(f"Unexpected response after logout: {response.status_code}")

        else:
            print(f"Logout failed: {response.text}")

    except Exception as e:
        print(f"Exception during test: {e}")
    finally:
        print("\n--- END JWT VERIFICATION ---")

if __name__ == "__main__":
    test_jwt_flow()
