from .models import Snippet
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

async def get_snippets(db: AsyncSession):
    result = await db.execute(select(Snippet))
    return result.scalars().all()
