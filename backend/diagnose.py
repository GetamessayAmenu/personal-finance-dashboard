#!/usr/bin/env python3

import sys
sys.path.append('/home/messay/Desktop/leapo/smartspend_full_starter/backend')

def diagnose_issue():
    print("🔍 Diagnosing backend issues...")

    try:
        # Test 1: Basic imports
        from app.database import engine, Base
        print("✅ Database imports work")

        # Test 2: Engine connection
        try:
            with engine.connect() as conn:
                result = conn.execute("SELECT 1")
                print("✅ Database connection works")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return

        # Test 3: Models import
        from app.models import User, Transaction, Budget
        print("✅ Models import work")

        # Test 4: Schemas import
        from app.schemas import UserCreate, TransactionCreate, BudgetCreate
        print("✅ Schemas import work")

        # Test 5: Database session
        from app.database import SessionLocal
        db = SessionLocal()
        print("✅ Database session created")

        # Test 6: Simple query
        try:
            users = db.query(User).all()
            print(f"✅ User query works: {len(users)} users")
        except Exception as e:
            print(f"❌ User query failed: {e}")
            return

        # Test 7: Transaction query
        try:
            transactions = db.query(Transaction).all()
            print(f"✅ Transaction query works: {len(transactions)} transactions")
        except Exception as e:
            print(f"❌ Transaction query failed: {e}")
            return

        db.close()
        print("✅ All database operations work!")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    diagnose_issue()
