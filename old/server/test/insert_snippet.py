import asyncio
from server.app.models import Snippet
from server.app.database import SessionLocal

async def add_sample_snippet():
    async with SessionLocal() as session:
        # Create a new snippet with all fields (including the new ones)
        new_snippet = Snippet(
            title="Hello World",
            content="print('Hello World')",
            language="Python",  # Assuming you're storing the language here
            created_at="2025-05-14T00:00:00Z",  # Assuming you're passing the time as string
            user_id="user_12345",  # Example user ID
            favorite=True,         # New column added
            solveCount=6           # New column added
        )
        
        # Add new snippet to the session
        session.add(new_snippet)
        
        # Commit the transaction asynchronously
        await session.commit()

# Run the async function
asyncio.run(add_sample_snippet())
