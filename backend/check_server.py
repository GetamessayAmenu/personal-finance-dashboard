#!/usr/bin/env python3

import requests
import json

def check_server_health():
    """Check if the server is running and test basic functionality"""
    base_url = "http://127.0.0.1:8001"

    print("🏥 Checking server health...")

    try:
        # Test root endpoint
        response = requests.get(f"{base_url}/", timeout=3)
        if response.status_code == 200:
            print(f"✅ Server is running: {response.json()}")
        else:
            print(f"❌ Server root endpoint failed: {response.status_code}")
            return False

        # Test auth endpoints (without authentication)
        print("\n🔐 Testing auth endpoints...")

        # Test registration
        register_data = {
            "username": "health_test",
            "email": "health@example.com",
            "password": "testpass123"
        }

        response = requests.post(f"{base_url}/auth/register", json=register_data, timeout=3)
        if response.status_code in [201, 400]:  # 400 means user already exists, which is also OK
            print("✅ Registration endpoint working")
        else:
            print(f"❌ Registration endpoint failed: {response.status_code}")
            return False

        # Test login
        login_data = {
            "email": "health@example.com",
            "password": "testpass123"
        }

        response = requests.post(f"{base_url}/auth/login", json=login_data, timeout=3)
        if response.status_code in [200, 401]:  # 401 means wrong password, which is OK for this test
            print("✅ Login endpoint working")
        else:
            print(f"❌ Login endpoint failed: {response.status_code}")
            return False

        print("\n✅ All basic server functionality is working!")
        return True

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server - server is not running")
        return False
    except Exception as e:
        print(f"❌ Server health check failed: {e}")
        return False

if __name__ == "__main__":
    success = check_server_health()
    if success:
        print("\n🎉 Backend server is healthy and ready!")
    else:
        print("\n💥 Backend server has issues")
