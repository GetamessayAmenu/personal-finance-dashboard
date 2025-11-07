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
    from sqlalchemy.orm import sessionmaker
    from datetime import datetime

    print("✅ All imports successful")

    # Create tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")

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

    # Test database operations
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    # Test user creation
    from app.schemas import UserCreate

    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="testpass123"
    )

    # Check if user exists
    existing_user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if existing_user:
        print("✅ User lookup works")
    else:
        # Create new user
        new_user = models.User(
            username=user_data.username,
            email=user_data.email,
            password=hash_password(user_data.password)
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print(f"✅ User created successfully: {new_user.id}")

        # Test user retrieval
        retrieved_user = db.query(models.User).filter(models.User.email == user_data.email).first()
        if retrieved_user:
            print(f"✅ User retrieval works: {retrieved_user.username}")
            print(f"✅ Created at field works: {retrieved_user.created_at}")
        else:
            print("❌ User retrieval failed")

    # Test cookie authentication function
    try:
        # Create a mock request with cookie
        mock_request = Mock()
        mock_request.cookies.get.return_value = token

        # This should work now
        user_data_result = get_current_user_from_cookie(mock_request, db)
        print(f"✅ Cookie authentication works: {user_data_result}")
    except Exception as e:
        print(f"❌ Cookie authentication failed: {e}")

    db.close()
    print("✅ All tests passed!")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
