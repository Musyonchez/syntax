import asyncio
from datetime import datetime, timezone
from server.app.models import Leaderboard
from server.app.database import SessionLocal

async def add_sample_leaderboard_entry():
    async with SessionLocal() as session:
        new_entry = Leaderboard(
            language="javascript",
            user_id="user_12345",
            snippet_id="snip_001",
            score=98,
            rank=1,
            similarity=0.85,
            difficulty=3,
            date_of_submission=datetime.now(timezone.utc),
        )
        session.add(new_entry)
        await session.commit()

asyncio.run(add_sample_leaderboard_entry())
