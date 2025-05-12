import strawberry
from typing import List, Optional
from sqlalchemy import text
from app.database import SessionLocal
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_items():
    return {"message": "List of items"}


# User GraphQL Type
@strawberry.type
class UserType:
    id: int
    email: str
    username: str
    image: str
    created_at: str


@strawberry.type
class Query:
    @strawberry.field
    async def getUsers(self) -> List[UserType]:
        async with SessionLocal() as session:
            result = await session.execute(
                text("SELECT id, email, username, image, created_at FROM users")
            )
            return [
                UserType(
                    id=row[0],
                    email=row[1],
                    username=row[2],
                    image=row[3],
                    created_at=row[4],
                )
                for row in result.fetchall()
            ]

    @strawberry.field
    async def getUser(self, email: str) -> Optional[UserType]:
        async with SessionLocal() as session:
            result = await session.execute(
                text(
                    "SELECT id, email, username, image, created_at FROM users WHERE email = :email"
                ),
                {"email": email},
            )
            row = result.fetchone()
            if row:
                return UserType(
                    id=row[0],
                    email=row[1],
                    username=row[2],
                    image=row[3],
                    created_at=row[4],
                )
            return None  # Or handle the case when user doesn't exist


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def add_user(
        self,
        username: str,
        email: str,
        image: str,
        created_at: str,
    ) -> UserType:
        async with SessionLocal() as session:
            # Step 1: Check if user exists
            result = await session.execute(
                text(
                    "SELECT id, username, email, image, created_at FROM users WHERE email = :email"
                ),
                {"email": email},
            )
            existing_user = result.fetchone()

            # Step 2: If found, return existing user
            if existing_user:
                return UserType(
                    id=existing_user[0],
                    username=existing_user[1],
                    email=existing_user[2],
                    image=existing_user[3],
                    created_at=existing_user[4],
                )

            # Step 3: If not found, insert new user
            insert_result = await session.execute(
                text(
                    """
                    INSERT INTO users (username, email, image, created_at)
                    VALUES (:username, :email, :image, :created_at)
                    RETURNING id, username, email, image, created_at
                """
                ),
                {
                    "username": username,
                    "email": email,
                    "image": image,
                    "created_at": created_at,
                },
            )
            new_user = insert_result.fetchone()
            await session.commit()

            return UserType(
                id=new_user[0],
                username=new_user[1],
                email=new_user[2],
                image=new_user[3],
                created_at=new_user[4],
            )
