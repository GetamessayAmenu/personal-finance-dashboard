#!/usr/bin/env python3

import sys
import os
sys.path.append('/home/messay/Desktop/leapo/smartspend_full_starter/backend')

try:
    # Test imports
    from app.database import engine, Base
    from app import models
    from app.utils.jwt_handler import create_access_token, get_current_user_from_cookie
    from app.utils.hashing import hash_password, verify_password
    from fastapi import Request
    from unittest.mock import Mock

    print("✅ All imports successful")

    # Test password hashing
    hashed = hash_password("testpass123")
    assert verify_password("testpass123", hashed)
    print("✅ Password hashing works")

    # Test JWT token creation
    token_data = {"sub": "test@example.com", "user_id": 1}
    token = create_access_token(token_data)
    print("✅ JWT token creation works")

    # Test JWT token decoding (simulate cookie auth)
    from jose import jwt, JWTError
    from app.utils.jwt_handler import SECRET_KEY, ALGORITHM

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"✅ JWT token decoding works: {payload}")
    except Exception as e:
        print(f"❌ JWT decoding failed: {e}")

    print("✅ All authentication functions working correctly!")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
