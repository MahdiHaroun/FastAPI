from fastapi import FastAPI , status , HTTPException , Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine  , get_db
from sqlalchemy.orm import Session 


models.Base.metadata.create_all(bind=engine)  # Create tables in the database


app = FastAPI()





    

#pydantic models
class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None

#pydantic models end
try: 
    conn = psycopg2.connect(host = "localhost" , database = "fastapiPOSTS" ,
                             user = "postgres" , password = "0816" , cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database connection successful")
except Exception as e:
    print("Database connection failed")
    print(f"Error: {e}")

    



@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()  # Fetch all posts from the database
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found")
    

    return {"data": posts} 







@app.post("/createpost" , status_code=status.HTTP_201_CREATED)
async def create_post (new_post: Post , db: Session = Depends(get_db)): #validate new_post as Post model
    new_post = models.Post(title=new_post.title, content=new_post.content, published=new_post.published) #or use new_post = models.Post(**new_post.dict())
    db.add(new_post)  # Add the new post to the session
    db.commit()  # Commit the transaction to save changes
    db.refresh(new_post)  # Refresh the instance to get the updated data

    return {"data": new_post}

#title: str
#conteent: str


@app.get("/posts/latest")
async def get_latest_post(db: Session = Depends(get_db)):
    latest_post = db.query(models.Post).order_by(models.Post.id.desc()).first()

    
    if not latest_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts available")
    return {"latest_post": latest_post}




@app.get("/posts/{id}")
async def get_post(id: int , db: Session = Depends(get_db)): # validate id as integer
    post = db.query(models.Post).filter(models.Post.id == id).first()
  
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    return {"post_detail": post}




@app.delete("/posts/{id}", status_code=status.HTTP_200_OK)
async def delete_post(id: int , db: Session = Depends(get_db)):
    delete_post = db.query(models.Post).filter(models.Post.id == id)
    if not delete_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    delete_post.delete(synchronize_session=False)  # Delete the post
    db.commit()  # Commit the transaction to save changes

    

    return {"message": "Post deleted successfully"}





@app.put("/posts/{id}", status_code=status.HTTP_200_OK)
async def update_post(id: int, update_post: PostUpdate , db: Session = Depends(get_db)):
    existing_post = db.query(models.Post).filter(models.Post.id == id)
    
    
    
    
    if not existing_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    existing_post.update({
        "title": update_post.title if update_post.title is not None else existing_post.first().title,                    #or use  existing_post.update(post.dict())
        "content": update_post.content if update_post.content is not None else existing_post.first().content,
        "published": update_post.published if update_post.published is not None else existing_post.first().published
    }, synchronize_session=False)
    db.commit()  # Commit the transaction to save changes
    
    
    return {"message": "Post updated successfully", "post": existing_post.first()}


@app.get("/sqlalchemy")
def test_posts(db : Session = Depends(get_db)):
    posts =  db.query(models.Post).all()
    return{"data": posts}
