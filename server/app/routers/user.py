import strawberry
from typing import List
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
    created_at: str


@strawberry.type
class Query:
    @strawberry.field
    async def getUsers(self) -> List[UserType]:
        async with SessionLocal() as session:
            result = await session.execute(
                text("SELECT id, email, username, created_at FROM users")
            )
            return [
                UserType(
                    id=row[0],
                    email=row[1],
                    username=row[2],
                    created_at=row[3]
                )
                for row in result.fetchall()
            ]
    
    @strawberry.field
    async def getUser(self, user_id: int) -> UserType:
        async with SessionLocal() as session:
            result = await session.execute(
                text("SELECT id, email, username, created_at FROM users WHERE id = :user_id"),
                {"user_id": user_id},
            )
            row = result.fetchone()
            if row:
                return UserType(
                    id=row[0],
                    email=row[1],
                    username=row[2],
                    created_at=row[3]
                )
            return None  # Or handle the case when user doesn't exist


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def add_user(
        self,
        username: str,
        email: str,
        password: str,  # For simplicity, storing the password directly (hash it before storing in production)
        created_at: str,
    ) -> UserType:
        async with SessionLocal() as session:
            result = await session.execute(
                text(
                    """
                    INSERT INTO users (username, email, password, created_at)
                    VALUES (:username, :email, :password, :created_at)
                    RETURNING id, username, email, created_at
                    """
                ),
                {
                    "username": username,
                    "email": email,
                    "password": password,  # Don't store raw passwords in real apps, hash it
                    "created_at": created_at,
                },
            )
            row = result.fetchone()
            await session.commit()
            return UserType(
                id=row[0],
                email=row[1],
                username=row[2],
                created_at=row[3]
            )
