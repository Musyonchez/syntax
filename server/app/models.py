from sqlalchemy import Column, Integer, String
from .database import Base

# Snippet Model
class Snippet(Base):
    __tablename__ = "snippets"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    language = Column(String)
    created_at = Column(String)  # Use UTC time as default
    user_id = Column(String)



# User Model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    image = Column(String, nullable=False)
    username = Column(String, index=True)
    created_at = Column(String)  # Default to current time


