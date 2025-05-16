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
    masked_content: Optional[str] = None
    answer: Optional[List[str]] = None


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
    async def getSnippet(
        self, 
        id: str, 
        ifmask: bool = False, 
        difficulty: Optional[int] = None
    ) -> Optional[SnippetType]:
        # Enforce rule: ifmask is True, difficulty must be provided
        if ifmask and difficulty is None:
            raise ValueError("Difficulty must be provided if ifmask is True.")

        async with SessionLocal() as session:
            result = await session.execute(
                text(
                    "SELECT id, title, content, language, created_at, user_id, favorite, solveCount FROM snippets WHERE id = :id"
                ),
                {"id": id},
            )
            if row := result.fetchone():

                if not ifmask:
                    return SnippetType(
                        id=row[0],
                        title=row[1],
                        content=row[2],
                        language=row[3],
                        created_at=row[4],
                        user_id=row[5],
                        favorite=row[6],
                        solveCount=row[7],
                    )

                original_content = row[2]
                language = row[3]
                masked_content, answer = mask_code_content(original_content, language, difficulty)

                return SnippetType(
                    id=row[0],
                    title=row[1],
                    content=row[2],  # override content
                    language=row[3],
                    created_at=row[4],
                    user_id=row[5],
                    favorite=row[6],
                    solveCount=row[7],
                    masked_content=masked_content,
                    answer=answer,
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
    


    @strawberry.mutation
    async def add_favorite(self, id: int, type: str = "single") -> List[SnippetType]:
        async with SessionLocal() as session:
            print(id,type)
            # Fetch current favorite value
            result = await session.execute(
                text("SELECT favorite FROM snippets WHERE id = :id"),
                {"id": id},
            )
            row = result.fetchone()
            if not row:
                raise ValueError("Snippet not found")

            current_favorite = row[0]
            new_favorite = not current_favorite

            # Update the favorite value
            await session.execute(
                text("UPDATE snippets SET favorite = :new_favorite WHERE id = :id"),
                {"new_favorite": new_favorite, "id": id},
            )
            await session.commit()

            # Decide what to return
            if type == "group":
                result = await session.execute(
                    text("SELECT id, title, content, language, created_at, user_id, favorite, solveCount FROM snippets")
                )
                rows = result.fetchall()
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
                    for row in rows
                ]
            else:  # type == "single"
                result = await session.execute(
                    text("SELECT id, title, content, language, created_at, user_id, favorite, solveCount FROM snippets WHERE id = :id"),
                    {"id": id},
                )
                row = result.fetchone()
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
                ]
