from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.user_schema import CreateUser, LoginUser, UserResponse, Token
from services import auth_user
from core.security import create_access_token, create_refresh_token
from api.deps import get_current_user
from models.user import User

router = APIRouter()

@router.post("/signup", response_model=UserResponse)
def signup(user: CreateUser, db: Session = Depends(get_db)):
    try:
        return auth_user.create_user(db=db, user=user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=Token)
def login(response: Response, user: LoginUser, db: Session = Depends(get_db)):
    try:
        db_user = auth_user.authenticate_user(db, email=user.email, password=user.password)
        access_token = create_access_token(data={"sub": db_user.email})
        refresh_token = create_refresh_token(data={"sub": db_user.email})
        
        auth_user.store_refresh_token(db, db_user.id, refresh_token)
        
        response.set_cookie(
            key="refresh_token", 
            value=refresh_token, 
            httponly=True, 
            secure=False, # Set to True in production with HTTPS
            samesite="lax"
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/refresh", response_model=Token)
def refresh_token(request: Request, response: Response, db: Session = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")
    
    db_token = auth_user.get_refresh_token(db, refresh_token)
    if not db_token or not db_token.is_active:
         raise HTTPException(status_code=401, detail="Invalid refresh token")
         
    # Rotation logic: Revoke old, issue new
    auth_user.revoke_refresh_token(db, refresh_token)
    
    # Get user to create new tokens
    user = db_token.user
    new_access_token = create_access_token(data={"sub": user.email})
    new_refresh_token = create_refresh_token(data={"sub": user.email})
    
    auth_user.store_refresh_token(db, user.id, new_refresh_token)
    
    response.set_cookie(
        key="refresh_token", 
        value=new_refresh_token, 
        httponly=True, 
        secure=False, 
        samesite="lax"
    )
    return {"access_token": new_access_token, "token_type": "bearer"}

@router.post("/logout")
def logout(request: Request, response: Response, db: Session = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token:
        auth_user.revoke_refresh_token(db, refresh_token)
    
    response.delete_cookie("refresh_token")
    return {"message": "Logged out successfully"}

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
