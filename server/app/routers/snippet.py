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
    language: str
    content: str
    created_at: str
    user_id: str

@strawberry.type
class SnippetSummaryType:
    id: int
    # title: str
    # content: str

@strawberry.type
class Query:
    @strawberry.field
    async def getSnippets(self) -> List[SnippetType]:
        async with SessionLocal() as session:
            print("was here")
            result = await session.execute(
                text(
                    "SELECT id, title, content, language, created_at, user_id FROM snippets"
                )
            )
            return [
                SnippetType(
                    id=row[0],
                    title=row[1],
                    content=row[2],
                    language=row[3],
                    created_at=row[4],
                    user_id=row[5],
                )
                for row in result.fetchall()
            ]


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def add_snippet(
        self,
        title: str,
        content: str,
        language: str,
        created_at: str,
        user_id: str,
    ) -> SnippetType:
        async with SessionLocal() as session:
            # Insert the new snippet
            print(title, content)
            result = await session.execute(
                text(
                    """
                    INSERT INTO snippets (title, content, language, created_at, user_id)
                    VALUES (:title, :content, :language, :created_at, :user_id)
                    RETURNING id, title, content, language, created_at, user_id
                """
                ),
                {
                    "title": title,
                    "content": content,
                    "language": language,
                    "created_at": created_at,
                    "user_id": user_id,
                },
            )
            # new_id = result.scalar()  # Get the newly inserted ID
            await session.commit()

            row = result.fetchone()
            # return SnippetType(id=row[0], title=row[1], content=row[2], language=row[3])

            return SnippetType(
                id=row[0],
                title=row[1],
                content=row[2],
                language=row[3],
                created_at=row[4],
                user_id=row[5],
            )
