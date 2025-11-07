#!/usr/bin/env python3

import os

# Fix the .env file
env_content = """DATABASE_URL=sqlite:///./finance_db.sqlite3
SECRET_KEY=your-secret-key-here-change-this-in-production
"""

with open('.env', 'w') as f:
    f.write(env_content.strip())

print("✅ .env file fixed with correct DATABASE_URL")

# Test the database connection
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv("DATABASE_URL")
print(f"📋 DATABASE_URL from .env: '{database_url}'")

try:
    engine = create_engine(database_url)
    print("✅ Database engine created successfully")
    print(f"📋 Engine URL: {engine.url}")
except Exception as e:
    print(f"❌ Database connection failed: {e}")

# Test imports
try:
    from app.database import get_db, Base
    from app.models import User
    print("✅ All imports successful")
except Exception as e:
    print(f"❌ Import failed: {e}")
