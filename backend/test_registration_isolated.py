#!/usr/bin/env python3

import sys
sys.path.append('/home/messay/Desktop/leapo/smartspend_full_starter/backend')

def test_registration_isolated():
    print("Testing registration function in isolation...")

    try:
        # Import components step by step
        from app.database import SessionLocal
        print("✅ Database imported")

        from app.models import User
        print("✅ Models imported")

        from app.utils.hashing import hash_password
        print("✅ Hashing imported")

        from app.schemas import UserCreate
        print("✅ Schemas imported")

        # Create test data
        user_data = UserCreate(
            username="isolated_test",
            email="isolated@example.com",
            password="testpass123"
        )
        print("✅ Test data created")

        # Test database session
        db = SessionLocal()
        print("✅ Database session created")

        # Test the exact query from registration
        try:
            existing = db.query(User).filter(User.email == user_data.email).first()
            print(f"✅ User lookup query works, existing user: {existing}")
        except Exception as e:
            print(f"❌ User lookup query failed: {e}")
            return False

        # Test user creation
        try:
            if not existing:
                new_user = User(
                    username=user_data.username,
                    email=user_data.email,
                    password=hash_password(user_data.password)
                )
                print("✅ User object created")

                db.add(new_user)
                print("✅ User added to session")

                db.commit()
                print("✅ Transaction committed")

                db.refresh(new_user)
                print(f"✅ User refreshed, ID: {new_user.id}")

            return True

        except Exception as e:
            print(f"❌ User creation failed: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            db.close()

    except Exception as e:
        print(f"❌ Import/component error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_registration_isolated()
    if success:
        print("\n🎉 Isolated registration test passed!")
    else:
        print("\n💥 Isolated registration test failed")
