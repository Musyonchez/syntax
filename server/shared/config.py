"""
Configuration management for SyntaxMem Cloud Functions
Centralizes environment variable loading and validation
"""
import os
from typing import List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for SyntaxMem"""
    
    # MongoDB Configuration
    MONGODB_URI: str = os.getenv("MONGODB_URI", "")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "syntaxmem")
    
    # JWT Configuration
    JWT_SECRET: str = os.getenv("JWT_SECRET", "")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRATION_HOURS: int = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))
    
    # Google OAuth Configuration
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    
    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
    
    # Function Configuration
    FUNCTION_REGION: str = os.getenv("FUNCTION_REGION", "us-central1")
    FUNCTION_MEMORY: str = os.getenv("FUNCTION_MEMORY", "512MB")
    FUNCTION_TIMEOUT: int = int(os.getenv("FUNCTION_TIMEOUT", "540"))
    
    # Environment Configuration
    NODE_ENV: str = os.getenv("NODE_ENV", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")
    
    # Admin Configuration
    ADMIN_EMAIL: str = os.getenv("ADMIN_EMAIL", "")
    
    @classmethod
    def validate(cls) -> None:
        """Validate required configuration"""
        required_vars = {
            "MONGODB_URI": cls.MONGODB_URI,
            "JWT_SECRET": cls.JWT_SECRET,
        }
        
        missing_vars = [name for name, value in required_vars.items() if not value]
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
        
        # Validate JWT secret length
        if len(cls.JWT_SECRET) < 32:
            raise ValueError("JWT_SECRET must be at least 32 characters long")
        
        # Validate Google OAuth config in production
        if cls.is_production():
            if not cls.GOOGLE_CLIENT_ID or not cls.GOOGLE_CLIENT_SECRET:
                raise ValueError("Google OAuth credentials required in production")
    
    @classmethod
    def is_development(cls) -> bool:
        """Check if running in development mode"""
        return cls.NODE_ENV.lower() in ["development", "dev"]
    
    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production mode"""
        return cls.NODE_ENV.lower() in ["production", "prod"]


# Global config instance
config = Config()

# Validate configuration on import
try:
    config.validate()
except ValueError as e:
    if config.is_development():
        print(f"⚠️  Configuration warning: {e}")
    else:
        raise e