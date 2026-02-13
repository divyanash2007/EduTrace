from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import DB_URL
from app.schemas.user_schema import CreateUser
from app.services.auth_user import create_user
import uuid
import sys

# Force unbuffered
sys.stdout.reconfigure(line_buffering=True)

def test_direct_signup():
    print("--- START DIRECT SERVICE TEST ---")
    try:
        engine = create_engine(DB_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        email = f"direct_signup_{str(uuid.uuid4())[:8]}@example.com"
        print(f"Creating user directly: {email}")
        
        user_in = CreateUser(
            name="Direct Test",
            email=email,
            password="password",
            role="tester"
        )
        
        user = create_user(db, user_in)
        print(f"User created: {user.id}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("--- END DIRECT SERVICE TEST ---")

if __name__ == "__main__":
    test_direct_signup()
