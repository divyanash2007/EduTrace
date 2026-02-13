from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.user_schema import CreateUser, LoginUser, UserResponse
from services import auth_user

router = APIRouter()

@router.post("/signup", response_model=UserResponse)
def signup(user: CreateUser, db: Session = Depends(get_db)):
    try:
        return auth_user.create_user(db=db, user=user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=UserResponse)
def login(user: LoginUser, db: Session = Depends(get_db)):
    try:
        return auth_user.authenticate_user(db, email=user.email, password=user.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
