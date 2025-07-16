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

    

#my_post = [{"id": 1, "title": "Post 1", "content": "Content of post 1", "published": True, "rating": 5}]

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/posts")
async def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}

@app.post("/createpost" , status_code=status.HTTP_201_CREATED)
async def create_post (new_post: Post): #validate new_post as Post model
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING  * """, # returting * means return all columns to the api 
                   (new_post.title, new_post.content, new_post.published))
    new_post = cursor.fetchone()
    conn.commit()  # Commit the transaction to save changes
    return {"data": new_post}

#title: str
#conteent: str


@app.get("/posts/latest")
async def get_latest_post():
    cursor.execute("""SELECT * FROM posts ORDER BY id DESC LIMIT 1 """)
    latest_post = cursor.fetchone()
    if not latest_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts available")
    return {"latest_post": latest_post}




@app.get("/posts/{id}")
async def get_post(id: int): # validate id as integer
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone()

  
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    return {"post_detail": post}




@app.delete("/posts/{id}", status_code=status.HTTP_200_OK)
async def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    conn.commit()  # Commit the transaction to save changes
    return {"message": "Post deleted successfully"}


@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
async def update_post(id: int, update_post: PostUpdate):
    # First get the existing post to use as defaults for None values
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    existing_post = cursor.fetchone()
    
    if not existing_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    # Use existing values if new values are None
    title = update_post.title if update_post.title is not None else existing_post['title']
    content = update_post.content if update_post.content is not None else existing_post['content']
    published = update_post.published if update_post.published is not None else existing_post['published']
    
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (title, content, published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    
    return {"message": "Post updated successfully", "post": updated_post}
