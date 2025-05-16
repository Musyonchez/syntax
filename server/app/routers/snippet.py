import strawberry
from typing import List, Optional
from sqlalchemy import text
from app.masking import mask_code_content  # Adjust import based on your structure


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
    favorite: bool
    solveCount: int


@strawberry.type
class SnippetSummaryType:
    id: int


@strawberry.type
class Query:
    @strawberry.field
    async def getSnippets(self) -> List[SnippetType]:
        async with SessionLocal() as session:
            print("was here")
            result = await session.execute(
                text(
                    "SELECT id, title, content, language, created_at, user_id, favorite, solveCount FROM snippets"
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
                    favorite=row[6],
                    solveCount=row[7],
                )
                for row in result.fetchall()
            ]

    @strawberry.field
    async def getSnippet(self, id: str) -> Optional[SnippetType]:
        async with SessionLocal() as session:
            print("was here")
            result = await session.execute(
                text(
                    "SELECT id, title, content, language, created_at, user_id, favorite, solveCount FROM snippets WHERE id = :id"
                ),
                {"id": id},
            )
            if row := result.fetchone():
                original_content = row[2]
                masked_content = mask_code_content(original_content, row[3])

                return SnippetType(
                    id=row[0],
                    title=row[1],
                    content=masked_content,  # masked content goes here
                    language=row[3],
                    created_at=row[4],
                    user_id=row[5],
                    favorite=row[6],
                    solveCount=row[7],
                )
        return None


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
                    INSERT INTO snippets (title, content, language, created_at, user_id, favorite, solveCount)
                    VALUES (:title, :content, :language, :created_at, :user_id, :favorite, :solveCount)
                    RETURNING id, title, content, language, created_at, user_id, favorite, solveCount
                """
                ),
                {
                    "title": title,
                    "content": content,
                    "language": language,
                    "created_at": created_at,
                    "user_id": user_id,
                    "favorite": False,
                    "solveCount": 0,
                },
            )
            # new_id = result.scalar()  # Get the newly inserted ID
            await session.commit()

            row = result.fetchone()
            # return SnippetType(id=row[0], title=row[1], content=row[2], language=row[3])

            return SnippetSummaryType(
                id=row[0],
            )
