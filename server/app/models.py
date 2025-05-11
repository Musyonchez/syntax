from sqlalchemy import Column, Integer, String
from .database import Base

class Snippet(Base):
    __tablename__ = "snippets"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    language = Column(String)
    created_at = Column(String)
    user_id = Column(Integer)
