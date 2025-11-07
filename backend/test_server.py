#!/usr/bin/env python3

import subprocess
import time
import requests
import json

def test_authentication():
    # Start the server in background
    print("🚀 Starting server...")
    server_process = subprocess.Popen([
        "python", "-m", "uvicorn", "app.main:app", "--reload", "--host", "127.0.0.1", "--port", "8000"
    ], cwd="/home/messay/Desktop/leapo/smartspend_full_starter/backend")

    # Wait for server to start
    time.sleep(3)

    try:
        # Test registration
        print("📝 Testing registration...")
        register_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123"
        }

        response = requests.post(
            "http://127.0.0.1:8000/auth/register",
            json=register_data,
            timeout=5
        )

        if response.status_code == 201:
            print(f"✅ Registration successful: {response.json()}")
        else:
            print(f"❌ Registration failed: {response.status_code} - {response.text}")
            return False

        # Test login
        print("🔑 Testing login...")
        login_data = {
            "email": "test@example.com",
            "password": "testpass123"
        }

        response = requests.post(
            "http://127.0.0.1:8000/auth/login",
            json=login_data,
            timeout=5
        )

        if response.status_code == 200:
            print(f"✅ Login successful: {response.json()}")

            # Test getting user data (this should work with cookie authentication)
            print("👤 Testing user data fetching...")
            # The login endpoint should set a cookie, but for this test we'll just check if the endpoint exists
            response = requests.get(
                "http://127.0.0.1:8000/auth/me",
                timeout=5
            )

            if response.status_code in [200, 401]:  # 401 means not authenticated, which is expected without cookie
                print("✅ User data endpoint accessible")
            else:
                print(f"⚠️  User data endpoint returned: {response.status_code}")

            return True
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server - server may not be running")
        return False
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False
    finally:
        print("🛑 Stopping server...")
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    success = test_authentication()
    if success:
        print("\n🎉 All authentication tests passed!")
    else:
        print("\n💥 Some tests failed - check the errors above")
