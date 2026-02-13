import sys
import traceback
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import DB_URL
from app.models.user import User
from app.services.auth_user import create_user
from app.schemas.user_schema import CreateUser as CreateUserSchema

# Disable any existing logging configuration that might interfere
# import logging
# logging.disable(logging.CRITICAL)

def test_connection():
    print("--- START TEST ---")
    try:
        print(f"Connecting to DB: {DB_URL}")
        engine = create_engine(DB_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        print("Database connection successful.")
        
        # Check if table exists
        try:
            users_count = db.query(User).count()
            print(f"Users table found. Count: {users_count}")
        except Exception as e:
            print("Failed to query users table. It might not exist.")
            print(e)
            return

        # Create user
        short_uuid = str(uuid.uuid4())[:8]
        unique_email = f"test_{short_uuid}@example.com"
        new_user = CreateUserSchema(
            name="Test User",
            email=unique_email,
            password="password",
            role="student"
        )
        print(f"Attempting to create user: {unique_email}")
        created_user = create_user(db, new_user)
        print(f"User created successfully. ID: {created_user.id}")
        
    except Exception:
        traceback.print_exc()
    finally:
        print("--- END TEST ---")

if __name__ == "__main__":
    test_connection()
