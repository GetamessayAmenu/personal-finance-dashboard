#!/usr/bin/env python3

import sys
sys.path.append('/home/messay/Desktop/leapo/smartspend_full_starter/backend')

def test_registration_directly():
    from app.database import SessionLocal, get_db
    from app.models import User
    from app.utils.hashing import hash_password
    from app.schemas import UserCreate

    print("Testing registration directly...")

    # Create database session
    db = SessionLocal()

    try:
        # Test data
        user_data = UserCreate(
            username="directtest",
            email="direct@example.com",
            password="testpass123"
        )

        # Check if user exists
        existing = db.query(User).filter(User.email == user_data.email).first()
        if existing:
            print("✅ User already exists")
            return True

        # Create new user
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            password=hash_password(user_data.password)
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        print(f"✅ User created successfully: {new_user.username} (ID: {new_user.id})")
        print(f"✅ Created at: {new_user.created_at}")

        # Test password verification
        from app.utils.hashing import verify_password
        is_valid = verify_password(user_data.password, new_user.password)
        print(f"✅ Password verification: {is_valid}")

        return True

    except Exception as e:
        print(f"❌ Registration failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = test_registration_directly()
    if success:
        print("\n🎉 Direct registration test passed!")
    else:
        print("\n💥 Direct registration test failed")
