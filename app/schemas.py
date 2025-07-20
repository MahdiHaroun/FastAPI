from pydantic import BaseModel , EmailStr
from typing import Optional
from datetime import datetime

#pydantic models
class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None


class User_Response(BaseModel):
    
    name: str
    email: EmailStr

    class Config:
        from_attributes = True  # Enable ORM mode to read data from SQLAlchemy models   

class PostResponse(BaseModel):
    title: str
    content: str
    published: bool
    id: int
    user_id : int
    created_at: datetime  # Changed from str to datetime
    owner : User_Response  
    

    class Config:
        from_attributes = True

class PostWithVotes(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        from_attributes = True

class User_create(BaseModel):
    name : str 
    email : EmailStr
    password : str




class User_login(BaseModel):   #used form instead 
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None



class Vote(BaseModel):
    post_id : int  
    dir : int  # 0 or 1, will validate in the route



#pydantic models end