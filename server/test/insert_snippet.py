import asyncio
from server.app.models import Snippet
from server.app.database import SessionLocal

async def add_sample_snippet():
    async with SessionLocal() as session:
        new_snippet = Snippet(title="Hello World", content="print('Hello World')")
        session.add(new_snippet)
        await session.commit()

asyncio.run(add_sample_snippet())



