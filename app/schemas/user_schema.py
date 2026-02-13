from pydantic import Field,BaseModel
from typing import Annotated

class CreateUser(BaseModel):
    name:Annotated[str,Field(...,min_length=3,max_length=50)]
    email:Annotated[str,Field(...,min_length=3,max_length=50)]
    password:Annotated[str,Field(...,min_length=3,max_length=50)]
    role:Annotated[str,Field(...,min_length=3,max_length=50)]
    
class LoginUser(BaseModel):
    email:Annotated[str,Field(...,min_length=3,max_length=50)]
    password:Annotated[str,Field(...,min_length=3,max_length=50)]

class UserResponse(BaseModel):
    id: Annotated[int,Field(...,min_length=1,max_length=50)]
    name: Annotated[str,Field(...,min_length=3,max_length=50)]
    email: Annotated[str,Field(...,min_length=3,max_length=50)]
    role: Annotated[str,Field(...,min_length=3,max_length=50)]
    created_at: Annotated[datetime,Field(...,min_length=3,max_length=50)]
    updated_at: Annotated[datetime,Field(...,min_length=3,max_length=50)]

