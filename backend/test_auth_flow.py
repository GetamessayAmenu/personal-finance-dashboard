#!/usr/bin/env python3

import sys
import os
sys.path.append('/home/messay/Desktop/leapo/smartspend_full_starter/backend')

try:
    # Test basic imports
    from app.database import get_db, engine, Base
    from app import models
    from app.utils.jwt_handler import create_access_token
    from app.utils.hashing import hash_password, verify_password
    from app.schemas import UserCreate, UserLogin
    from fastapi import Request
    from unittest.mock import Mock
    from sqlalchemy.orm import sessionmaker

    print("✅ All imports successful")

    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables ready")

    # Test database session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Test user registration
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="testpass123"
    )

    # Create a test database session
    db = SessionLocal()

    # Check if user already exists
    existing_user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if existing_user:
        print(f"✅ User already exists: {existing_user.username}")
        test_user = existing_user
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
        test_user = new_user
        print(f"✅ User created successfully: {test_user.username} (ID: {test_user.id})")

    # Test password verification
    login_data = UserLogin(email="test@example.com", password="testpass123")
    db_user = db.query(models.User).filter(models.User.email == login_data.email).first()

    if db_user and verify_password(login_data.password, db_user.password):
        print("✅ Password verification successful")

        # Test JWT token creation
        token_data = {"sub": db_user.email, "user_id": db_user.id}
        token = create_access_token(token_data)
        print("✅ JWT token created successfully")

        # Test cookie authentication function
        try:
            from app.utils.jwt_handler import get_current_user_from_cookie

            # Create a mock request with cookie
            mock_request = Mock()
            mock_request.cookies.get.return_value = token

            # This should work now
            user_data_result = get_current_user_from_cookie(mock_request, db)
            print(f"✅ Cookie authentication works: {user_data_result}")
        except Exception as e:
            print(f"❌ Cookie authentication failed: {e}")

    else:
        print("❌ Password verification failed")

    db.close()
    print("✅ All authentication tests passed!")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
