from sqlalchemy.orm import Session
from models.user import User
from schemas.user_schema import CreateUser
from utils.password_hash import hash_password, verify_password

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: CreateUser):
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise ValueError("Email already registered")
    
    hashed_password = hash_password(user.password)
    db_user = User(
        full_name=user.name,
        email=user.email,
        password_hash=hashed_password,
        role=user.role
    )
    db.add(db_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Error during Creating user!!")
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        raise ValueError("Invalid email or password")
    if not verify_password(password, user.password_hash):
        raise ValueError("Invalid email or password")
    return user
