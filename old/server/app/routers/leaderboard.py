from sqlalchemy import select
from app.models import Leaderboard
from typing import List, Optional
import strawberry
from fastapi import APIRouter


from app.database import SessionLocal

router = APIRouter()


@router.get("/")
async def list_items():
    return {"message": "List of leaderboard items"}


VALID_LANGUAGES = {"Python", "Javascript"}  # Easily extendable
VALID_TIME_CATEGORIES = {
    "daily",
    "weekly",
    "monthly",
    "half-yearly",
    "yearly",
    "all-time",
}


@strawberry.type
class LeaderboardType:
    id: int
    leaderboard_type: str
    user_id: str
    userName: str
    snippet_id: str
    score: float
    rank: Optional[int]
    similarity: Optional[float]
    difficulty: Optional[int]
    date_of_submission: Optional[str]  # Will return ISO string


@strawberry.type
class LeaderboardSummaryType:
    category: str
    entries: List[LeaderboardType]


@strawberry.type
class Query:

    @strawberry.field
    async def get_leaderboard(self, category: str) -> Optional[LeaderboardSummaryType]:
        async with SessionLocal() as session:
            result = await session.execute(
                select(Leaderboard)
                .where(Leaderboard.leaderboard_type == category)
                .order_by(Leaderboard.score.desc())
            )
            entries = result.scalars().all()

            if not entries:
                return None

            # Update ranks based on order
            for index, entry in enumerate(entries, start=1):
                entry.rank = index

            entry_objs = [
                LeaderboardType(
                    id=entry.id,
                    leaderboard_type=entry.leaderboard_type,
                    user_id=entry.user_id,
                    userName=entry.userName,
                    snippet_id=entry.snippet_id,
                    score=entry.score,
                    rank=entry.rank,
                    similarity=entry.similarity,
                    difficulty=entry.difficulty,
                    date_of_submission=entry.date_of_submission,
                )
                for entry in entries
            ]

            return LeaderboardSummaryType(category=category, entries=entry_objs)


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def add_leaderboard(
        self,
        language: str,
        user_id: str,
        userName: str,
        snippet_id: str,
        score: float,
        similarity: float,
        difficulty: int,
        date_of_submission: str,
    ) -> bool:
        if language not in VALID_LANGUAGES:
            return False

        print("i was here leaderboard")
        success = False

        async with SessionLocal() as session:
            for time_category in VALID_TIME_CATEGORIES:
                category = f"{time_category}_{language}"

                # Create the new leaderboard entry
                new_entry = Leaderboard(
                    leaderboard_type=category,
                    user_id=user_id,
                    userName=userName,
                    snippet_id=snippet_id,
                    score=score,
                    similarity=similarity,
                    difficulty=difficulty,
                    date_of_submission=date_of_submission,
                )

                # Get current top 10
                result = await session.execute(
                    select(Leaderboard)
                    .where(Leaderboard.leaderboard_type == category)
                    .order_by(Leaderboard.score.desc())
                    .limit(10)
                )
                top_entries = result.scalars().all()

                # Check if new entry qualifies
                qualifies = len(top_entries) < 10 or any(score > entry.score for entry in top_entries)

                if qualifies:
                    session.add(new_entry)
                    await session.flush()  # Add entry to session to reflect it in DB for re-querying

                    # Get updated full list sorted by score
                    result = await session.execute(
                        select(Leaderboard)
                        .where(Leaderboard.leaderboard_type == category)
                        .order_by(Leaderboard.score.desc())
                    )
                    all_entries = result.scalars().all()

                    # Trim to top 10
                    for extra_entry in all_entries[10:]:
                        await session.delete(extra_entry)

                    success = True

            if success:
                await session.commit()

        return success

