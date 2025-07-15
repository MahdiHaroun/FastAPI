from fastapi import FastAPI , status , HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None


try: 
    conn = psycopg2.connect(host = "localhost" , database = "fastapiPOSTS" ,
                             user = "postgres" , password = "0816" , cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database connection successful")
except Exception as e:
    print("Database connection failed")
    print(f"Error: {e}")

    

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


@app.delete("/posts/{id}", status_code=status.HTTP_200_OK)
async def delete_post(id: int):
    global my_post
    
    # Check if the post exists before deletion
    post_found = False
    for p in my_post:
        if p["id"] == id:
            post_found = True
            break

    
    if not post_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    # Remove the post
    my_post = [p for p in my_post if p["id"] != id]
    
    return {"message": "Post deleted successfully"}


@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
async def update_post(id: int, update_post: PostUpdate):
    global my_post
    
    # Find the post to update
    post_found = False
    for i, p in enumerate(my_post):
        if p["id"] == id:
            post_found = True
            # Update the post with new values
            if update_post.title is not None:
                my_post[i]["title"] = update_post.title
            if update_post.content is not None:
                my_post[i]["content"] = update_post.content
            if update_post.published is not None:
                my_post[i]["published"] = update_post.published
            
            break
    
    if not post_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    return {"message": "Post updated successfully", "post": my_post[i]}
