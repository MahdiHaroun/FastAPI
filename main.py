from fastapi import FastAPI , status , HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_post = [{"id": 1, "title": "Post 1", "content": "Content of post 1", "published": True, "rating": 5}]

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/posts")
async def get_posts():
    return {"data": my_post}

@app.post("/createpost" , status_code=status.HTTP_201_CREATED)
async def create_post (new_post: Post): #validate new_post as Post model
    post_dict = new_post.dict()
    post_dict['id'] = len(my_post) + 1
    my_post.append(post_dict)
    return {"data": my_post}

#title: str
#conteent: str


@app.get("/posts/latest")
async def get_latest_post():
    if not my_post:
        return {"error": "No posts available"}
    
    latest_post = my_post[-1]
    return {"latest_post": latest_post}




@app.get("/posts/{id}")
async def get_post(id: int): # validate id as integer
    post = None
    for p in my_post: 
        if p["id"] == id: 
            post = p 
            break
    
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    return {"post_detail": post}




