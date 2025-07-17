from .. import models, schemas , oauth2
from ..database import  get_db
from fastapi import FastAPI , status , HTTPException , Depends , APIRouter
from sqlalchemy.orm import Session 


router = APIRouter(

    prefix="/posts", 
    tags=["posts"]
)






@router.get("/")
async def get_posts(db: Session = Depends(get_db) , user_id :int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()  # Fetch all posts from the database
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found")
    

    return posts







@router.post("/" , status_code=status.HTTP_201_CREATED , response_model=schemas.PostResponse)  # Use response_model to return PostResponse schema
async def create_post (new_post: schemas.Post , db: Session = Depends(get_db) , 
                       user_id :int = Depends(oauth2.get_current_user)): #validate new_post as Post model
    print(user_id)  
    new_post = models.Post(title=new_post.title, content=new_post.content, published=new_post.published) #or use new_post = models.Post(**new_post.dict())
    db.add(new_post)  # Add the new post to the session
    db.commit()  # Commit the transaction to save changes
    db.refresh(new_post)  # Refresh the instance to get the updated data

    return new_post

#title: str
#conteent: str


@router.get("/latest" ,  response_model=schemas.PostResponse)  # Use response_model to return PostResponse schema
async def get_latest_post(db: Session = Depends(get_db) , user_id :int = Depends(oauth2.get_current_user)) :
    latest_post = db.query(models.Post).order_by(models.Post.id.desc()).first()

    
    if not latest_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts available")
    return latest_post








@router.get("/{id}", response_model=schemas.PostResponse)  # Use response_model to return PostResponse schema
async def get_post(id: int , db: Session = Depends(get_db) , user_id :int = Depends(oauth2.get_current_user)): # validate id as integer
    post = db.query(models.Post).filter(models.Post.id == id).first()
  
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    return  post




@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_post(id: int , db: Session = Depends(get_db) , user_id :int = Depends(oauth2.get_current_user)):
    delete_post = db.query(models.Post).filter(models.Post.id == id)
    if not delete_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    delete_post.delete(synchronize_session=False)  # Delete the post
    db.commit()  # Commit the transaction to save changes

    

    return {"message": "Post deleted successfully"}





@router.put("/{id}", status_code=status.HTTP_200_OK , response_model=schemas.PostResponse)  # Use response_model to return PostResponse schema
async def update_post(id: int, update_post: schemas.PostUpdate , db: Session = Depends(get_db) , user_id :int = Depends(oauth2.get_current_user)):
    existing_post = db.query(models.Post).filter(models.Post.id == id)
    
    
    
    
    if not existing_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    existing_post.update({
        "title": update_post.title if update_post.title is not None else existing_post.first().title,                    #or use  existing_post.update(post.dict())
        "content": update_post.content if update_post.content is not None else existing_post.first().content,
        "published": update_post.published if update_post.published is not None else existing_post.first().published
    }, synchronize_session=False)
    db.commit()  # Commit the transaction to save changes
    
    
    return  existing_post.first()