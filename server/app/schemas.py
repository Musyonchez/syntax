from pydantic import BaseModel

class SnippetCreate(BaseModel):
    title: str
    content: str
