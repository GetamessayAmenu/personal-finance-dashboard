#!/usr/bin/env python3

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check what DATABASE_URL contains
database_url = os.getenv("DATABASE_URL")
print(f"Raw DATABASE_URL: '{database_url}'")

# Check if there are any other environment variables that might be interfering
for key, value in os.environ.items():
    if 'DATABASE' in key or 'SQLITE' in key or 'DB' in key:
        print(f"{key}={value}")

# Try to manually set a correct DATABASE_URL
os.environ["DATABASE_URL"] = "sqlite:///./finance_db.sqlite3"
corrected_url = os.getenv("DATABASE_URL")
print(f"Corrected DATABASE_URL: '{corrected_url}'")
