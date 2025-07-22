from fastapi import FastAPI 
from . import models 
from .database import engine  
from .routers import posts, user , auth , vote




models.Base.metadata.create_all(bind=engine)  # Create tables in the database


app = FastAPI()

app.include_router(posts.router)  # Include the posts router
app.include_router(user.router)  # Include the user router
app.include_router(auth.router)  # Include the auth router
app.include_router(vote.router)  # Include the vote router


@app.get("/")  # Root endpoint
def root():
    return {"message": "Welcome to the API!!"}