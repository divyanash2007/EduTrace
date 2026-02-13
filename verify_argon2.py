import requests
import json
import uuid

BASE_URL = "http://localhost:8000"

def test_signup():
    print("Testing Signup...")
    # Use a random email to avoid collision
    short_uuid = str(uuid.uuid4())[:8]
    email = f"argon2_test_{short_uuid}@example.com"
    payload = {
        "name": "Argon User",
        "email": email,
        "password": "password123",
        "role": "student"
    }
    try:
        response = requests.post(f"{BASE_URL}/auth/signup", json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return email
    except Exception as e:
        print(f"Signup failed: {e}")
        return None

def test_login(email):
    print("\nTesting Login...")
    if not email:
        print("Skipping login test due to signup failure")
        return

    payload = {
        "email": email,
        "password": "password123"
    }
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Login failed: {e}")

if __name__ == "__main__":
    email = test_signup()
    test_login(email)
