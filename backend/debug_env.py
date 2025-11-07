#!/usr/bin/env python3

import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
print(f"DATABASE_URL from environment: '{DATABASE_URL}'")
print(f"DATABASE_URL type: {type(DATABASE_URL)}")
print(f"DATABASE_URL length: {len(DATABASE_URL) if DATABASE_URL else 'None'}")
