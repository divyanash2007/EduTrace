from pydantic import Field,EmailStr ,BaseModel
from typing import Annotated
from datetime import datetime
from uuid import UUID

class CreateUser(BaseModel):
    name: Annotated[str, Field(..., min_length=3, max_length=50)]
    email: Annotated[EmailStr, Field(..., min_length=3, max_length=50)]
    password: Annotated[str, Field(..., min_length=3, max_length=50)]
    role: Annotated[str, Field(..., min_length=3, max_length=50)]
    
class LoginUser(BaseModel):
    email: Annotated[EmailStr, Field(..., min_length=3, max_length=50)]
    password: Annotated[str, Field(..., min_length=3, max_length=50)]

class UserResponse(BaseModel):
    id: UUID
    full_name: Annotated[str, Field(..., min_length=3, max_length=50)]
    email: Annotated[EmailStr, Field(..., min_length=3, max_length=50)]
    role: Annotated[str, Field(..., min_length=3, max_length=50)]
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

