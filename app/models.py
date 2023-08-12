from sqlalchemy import Column, Integer, String,ForeignKey,DateTime,func

from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True,nullable=False)
    email = Column(String, unique=True,nullable=False)
    password = Column(String,nullable=False)
    ph_no = Column(String)

class Post(Base):
    __tablename__="posts"
    id = Column(Integer, primary_key=True,nullable=False) 
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)
    owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    created_at=Column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    owner=relationship('User')


class Vote(Base):
    __tablename__="votes"
    post_id=Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),nullable=False,primary_key=True)
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False,primary_key=True)
    
    
    