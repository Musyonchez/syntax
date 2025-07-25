"""
MongoDB database connection utilities for SyntaxMem Flask functions
"""
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB configuration
MONGODB_URI = os.getenv('MONGODB_URI')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'syntaxmem')

if not MONGODB_URI:
    raise ValueError("MONGODB_URI environment variable is required")


async def get_database():
    """Get MongoDB database instance - create new connection for each request in serverless"""
    try:
        # Create a new client for each request to avoid event loop conflicts
        client = AsyncIOMotorClient(MONGODB_URI)
        database = client[DATABASE_NAME]
        
        # Test connection
        await client.admin.command('ping')
        return database
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise


# Collection getters
async def get_users_collection():
    """Get users collection"""
    db = await get_database()
    return db.users


async def get_snippets_collection():
    """Get snippets collection"""
    db = await get_database()
    return db.snippets


async def get_practice_sessions_collection():
    """Get practice sessions collection"""
    db = await get_database()
    return db.practice_sessions


async def get_leaderboard_collection():
    """Get leaderboard collection"""
    db = await get_database()
    return db.leaderboard


async def get_forum_posts_collection():
    """Get forum posts collection"""
    db = await get_database()
    return db.forum_posts