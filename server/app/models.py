from sqlalchemy import Boolean, Column, Integer, String
from .database import Base

# Snippet Model
class Snippet(Base):
    __tablename__ = "snippets"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    language = Column(String)
    created_at = Column(String)
    user_id = Column(String)
    favorite = Column(Boolean, default=False)
    solveCount = Column(Integer, default=0)  # Use Integer instead of Number




# User Model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    image = Column(String, nullable=False)
    username = Column(String, index=True)
    created_at = Column(String)  # Default to current time


