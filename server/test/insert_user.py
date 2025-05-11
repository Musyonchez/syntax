import asyncio
from server.app.models import User  # Change to User model
from server.app.database import SessionLocal

async def add_sample_user():
    async with SessionLocal() as session:
        new_user = User(name="john_doe", email="john@example.com", password="securepass")  # Use user-related fields
        session.add(new_user)
        await session.commit()

asyncio.run(add_sample_user())
