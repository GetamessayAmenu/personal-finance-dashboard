#!/usr/bin/env python3

import requests
import json

def test_complete_backend():
    """Test all backend functionality"""
    base_url = "http://127.0.0.1:8001"

    print("🚀 Starting comprehensive backend test...")

    # Step 1: Test basic server connectivity
    print("\n🌐 Step 1: Testing server connectivity...")
    try:
        response = requests.get(f"{base_url}/", timeout=3)
        if response.status_code == 200:
            print(f"✅ Server is running: {response.json()}")
        else:
            print(f"❌ Server error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        return False

    # Step 2: Test registration
    print("\n📝 Step 2: Testing registration...")
    register_data = {
        "username": "test_backend",
        "email": "backend_test@example.com",
        "password": "testpass123"
    }

    try:
        response = requests.post(f"{base_url}/auth/register", json=register_data, timeout=3)
        if response.status_code in [201, 400]:  # 400 means already exists
            print("✅ Registration endpoint working")
        else:
            print(f"❌ Registration failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return False

    # Step 3: Test login
    print("\n🔑 Step 3: Testing login...")
    login_data = {
        "email": "backend_test@example.com",
        "password": "testpass123"
    }

    try:
        response = requests.post(f"{base_url}/auth/login", json=login_data, timeout=3)
        if response.status_code == 200:
            print(f"✅ Login successful")
            cookies = response.cookies
        else:
            print(f"❌ Login failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Login error: {e}")
        return False

    # Step 4: Test user data
    print("\n👤 Step 4: Testing user data...")
    try:
        response = requests.get(f"{base_url}/auth/me", cookies=cookies, timeout=3)
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ User data: {user_data['username']}")
        else:
            print(f"❌ User data failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ User data error: {e}")
        return False

    # Step 5: Test transactions
    print("\n💰 Step 5: Testing transactions...")
    try:
        response = requests.get(f"{base_url}/transactions/", cookies=cookies, timeout=3)
        if response.status_code == 200:
            transactions = response.json()
            print(f"✅ Transactions loaded: {len(transactions)} transactions")
        else:
            print(f"❌ Transactions failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Transactions error: {e}")
        return False

    print("\n🎉 All backend tests passed!")
    return True

if __name__ == "__main__":
    success = test_complete_backend()
    if success:
        print("\n✅ Backend is fully working!")
    else:
        print("\n❌ Backend has issues")
