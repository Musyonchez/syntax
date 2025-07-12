"""
MongoDB database connection and utilities for SyntaxMem
"""
import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
from dotenv import load_dotenv

# Import configuration
from .config import config

# MongoDB configuration from config
MONGODB_URI = config.MONGODB_URI
DATABASE_NAME = config.DATABASE_NAME

# Global client instance
_client: Optional[AsyncIOMotorClient] = None
_database = None


async def get_database():
    """Get MongoDB database instance"""
    global _client, _database
    
    if _client is None:
        _client = AsyncIOMotorClient(MONGODB_URI)
        _database = _client[DATABASE_NAME]
        
        # Test connection
        try:
            await _client.admin.command('ping')
            print("Successfully connected to MongoDB!")
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")
            raise
    
    return _database


async def close_database():
    """Close MongoDB connection"""
    global _client
    if _client:
        _client.close()
        _client = None


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


async def get_forum_comments_collection():
    """Get forum comments collection"""
    db = await get_database()
    return db.forum_comments


async def get_user_votes_collection():
    """Get user votes collection"""
    db = await get_database()
    return db.user_votes


# Database initialization
async def init_database():
    """Initialize database with indexes and default data"""
    db = await get_database()
    
    # Create indexes for better performance
    await db.users.create_index("email", unique=True)
    await db.users.create_index("googleId", unique=True)
    
    await db.snippets.create_index([("type", 1), ("language", 1)])
    await db.snippets.create_index("author")
    
    await db.practice_sessions.create_index([("userId", 1), ("createdAt", -1)])
    await db.practice_sessions.create_index("snippetId")
    
    await db.leaderboard.create_index([("language", 1), ("score", -1)])
    await db.leaderboard.create_index("userId")
    
    await db.forum_posts.create_index([("createdAt", -1)])
    await db.forum_comments.create_index([("postId", 1), ("createdAt", 1)])
    
    await db.user_votes.create_index([("userId", 1), ("targetId", 1)], unique=True)
    
    print("Database indexes created successfully!")


if __name__ == "__main__":
    # Test connection
    async def test():
        await init_database()
        await close_database()
    
    asyncio.run(test())