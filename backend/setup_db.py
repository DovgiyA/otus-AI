#!/usr/bin/env python
"""
Setup script to create PostgreSQL database and tables.
Run this if database doesn't exist or needs reset.
"""
import sys
import os
import subprocess

# Try to create database using createdb command
try:
    subprocess.run(
        ["sudo", "-n", "createdb", "-U", "postgres", "mini_survey_db"],
        capture_output=True,
        timeout=10
    )
    print("✓ Database created using createdb")
except Exception as e:
    print(f"Could not create database: {e}")
    print("Database will be created within the app, or you can set up manually.")

# Now run database initialization
try:
    sys.path.insert(0, '/workspaces/otus-AI/backend')
    from database import init_db
    from config import settings
    
    print(f"\nDatabase URL: {settings.DATABASE_URL}")
    print("Initializing database schema...")
    init_db()
    print("✓ Database initialized successfully")
except Exception as e:
    print(f"✗ Error initializing database: {e}")
    print("\nMake sure PostgreSQL is running:")
    print("  sudo service postgresql start")
    sys.exit(1)
