from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import DB_URL
from app.models.user import User
from app.services.auth_user import create_user
from app.schemas.user_schema import CreateUser as CreateUserSchema
import uuid

def test_connection():
    try:
        engine = create_engine(DB_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        print("Database connection successful.")
        
        # Try to query users
        users = db.query(User).limit(1).all()
        print(f"Users table exists. Found {len(users)} users.")
        
        # Try to create a dummy user to verify schema matches
        # unique email
        unique_email = f"test_{uuid.uuid4()}@example.com"
        new_user = CreateUserSchema(
            name="Test User",
            email=unique_email,
            password="password",
            role="student"
        )
        created_user = create_user(db, new_user)
        print(f"User created successfully: {created_user.id}")
        
    except Exception as e:
        print(f"Database error: {e}")

if __name__ == "__main__":
    test_connection()
