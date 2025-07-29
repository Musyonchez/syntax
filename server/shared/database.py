import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional

class Database:
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.db = None
    
    async def connect(self):
        """Connect to MongoDB"""
        if not self.client:
            mongodb_uri = os.getenv("MONGODB_URI")
            database_name = os.getenv("DATABASE_NAME", "syntaxmem")
            
            if not mongodb_uri:
                raise ValueError("MONGODB_URI environment variable not set")
            
            self.client = AsyncIOMotorClient(mongodb_uri)
            self.db = self.client[database_name]
    
    async def get_users_collection(self):
        """Get users collection"""
        if self.db is None:
            await self.connect()
        return self.db.users
    
    async def get_refresh_tokens_collection(self):
        """Get refresh tokens collection"""
        if self.db is None:
            await self.connect()
        return self.db.refresh_tokens
    
    def close(self):
        """Close database connection"""
        if self.client:
            self.client.close()

# Global database instance
db = Database()