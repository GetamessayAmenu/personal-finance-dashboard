#!/usr/bin/env python3

import requests
import json

def test_registration_and_login():
    base_url = "http://127.0.0.1:8001"

    # Test registration
    print("📝 Testing registration...")
    register_data = {
        "username": "testuser123",
        "email": "test123@example.com",
        "password": "testpass123"
    }

    try:
        response = requests.post(f"{base_url}/auth/register", json=register_data, timeout=5)
        print(f"Registration status: {response.status_code}")

        if response.status_code == 201:
            print(f"✅ Registration successful: {response.json()}")

            # Test login
            print("🔑 Testing login...")
            login_data = {
                "email": "test123@example.com",
                "password": "testpass123"
            }

            response = requests.post(f"{base_url}/auth/login", json=login_data, timeout=5)
            print(f"Login status: {response.status_code}")

            if response.status_code == 200:
                print(f"✅ Login successful: {response.json()}")

                # Test getting user data
                print("👤 Testing user data fetching...")
                response = requests.get(f"{base_url}/auth/me", timeout=5)
                print(f"User data status: {response.status_code}")

                if response.status_code == 200:
                    print(f"✅ User data fetched: {response.json()}")
                    return True
                else:
                    print(f"❌ User data fetch failed: {response.text}")
                    return False
            else:
                print(f"❌ Login failed: {response.text}")
                return False
        else:
            print(f"❌ Registration failed: {response.text}")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_registration_and_login()
    if success:
        print("\n🎉 All authentication tests passed!")
    else:
        print("\n💥 Some tests failed")
