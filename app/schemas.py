from pydantic import BaseModel , EmailStr
from typing import Optional
#pydantic models
class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None

class PostResponse(BaseModel):
    title: str
    content: str
    published: bool

    class Config:
        from_attributes = True

class User_create(BaseModel):
    name : str 
    email : EmailStr
    password : str


class User_Response(BaseModel):
    
    name: str
    email: EmailStr

    class Config:
        from_attributes = True  # Enable ORM mode to read data from SQLAlchemy models

class User_login(BaseModel):
    email: EmailStr
    password: str

#pydantic models end