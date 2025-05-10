import asyncio
from server.app.database import Base, engine
from server.app.models import Snippet  # noqa: F401  # needed for table creation

async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(create_db())
