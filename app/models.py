from .database import Base 
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql import text

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True , nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default=text('True'), default=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)

