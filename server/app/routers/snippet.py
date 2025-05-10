import strawberry
from typing import List
from sqlalchemy import text  # <-- Add this import

# from app.models import Snippet
from app.database import SessionLocal

# from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_items():
    return {"message": "List of items"}


@strawberry.type
class SnippetType:
    id: int
    title: str
    content: str


@strawberry.type
class Query:
    @strawberry.field
    async def snippets(self) -> List[SnippetType]:
        async with SessionLocal() as session:
            result = await session.execute(
                text("SELECT id, title, content FROM snippets")  # <-- Wrap in text()
            )
            return [
                SnippetType(id=row[0], title=row[1], content=row[2])
                for row in result.fetchall()
            ]
