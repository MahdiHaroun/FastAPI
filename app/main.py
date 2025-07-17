from fastapi import FastAPI , status , HTTPException , Depends
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models , schemas , utils
from .database import engine  , get_db
from sqlalchemy.orm import Session 
from .routers import posts, user , auth




models.Base.metadata.create_all(bind=engine)  # Create tables in the database


app = FastAPI()



try: 
    conn = psycopg2.connect(host = "localhost" , database = "fastapiPOSTS" ,
                             user = "postgres" , password = "0816" , cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database connection successful")
except Exception as e:
    print("Database connection failed")
    print(f"Error: {e}")

    





app.include_router(posts.router)  # Include the posts router
app.include_router(user.router)  # Include the user router
app.include_router(auth.router)  # Include the auth router
