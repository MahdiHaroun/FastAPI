from .database import Base 
from sqlalchemy import Column, Integer, String, Boolean , ForeignKey 
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship
class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True , nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default=text('True'), default=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    user_id  = Column(Integer , ForeignKey('users.id' , ondelete= "CASCADE"), nullable=False )  # Assuming a foreign key relationship with User model
    

    owner = relationship("User")  


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True , nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)



class Vote(Base):
    __tablename__ = 'votes'
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete="CASCADE"), primary_key=True)
    
