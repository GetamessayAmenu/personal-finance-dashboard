#!/usr/bin/env python3

import requests
import json

def test_server():
    """Test if the server is working"""
    base_url = "http://127.0.0.1:8001"

    print("🧪 Testing server...")

    try:
        # Test root endpoint
        response = requests.get(f"{base_url}/", timeout=3)
        if response.status_code == 200:
            print(f"✅ Server is running: {response.json()}")
            return True
        else:
            print(f"❌ Server error: {response.status_code}")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_server()
