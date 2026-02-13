import requests
import json

BASE_URL = "http://localhost:8000"

def test_signup():
    print("Testing Signup...")
    payload = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123",
        "role": "student"
    }
    try:
        response = requests.post(f"{BASE_URL}/auth/signup", json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Signup failed: {e}")

def test_login():
    print("\nTesting Login...")
    payload = {
        "email": "test@example.com",
        "password": "password123"
    }
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Login failed: {e}")

if __name__ == "__main__":
    test_signup()
    test_login()
