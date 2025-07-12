from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
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


# leaderboard Model
class Leaderboard(Base):
    __tablename__ = "leaderboard"

    id = Column(Integer, primary_key=True, index=True)
    leaderboard_type = Column(String, nullable=False)  # e.g., 'python', 'javascript'
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    userName = Column(String, ForeignKey("users.username"), nullable=False)
    snippet_id = Column(String, ForeignKey("snippets.id"), nullable=False)
    score = Column(Integer, nullable=False)
    rank = Column(Integer, nullable=True)  # optional, for ordering
    similarity = Column(Float, nullable=True)    # new field
    difficulty = Column(Integer, nullable=True)  # new field
    date_of_submission = Column(String)  # new field