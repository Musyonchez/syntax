"""
Forum Cloud Function for SyntaxMem
Handles forum posts and discussions using Flask
"""

import asyncio
import os
import re
from datetime import datetime
from typing import Any, Dict, List, Optional

import functions_framework
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

# Create Flask app
app = Flask(__name__)

# Configure CORS with environment-based origins
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:3001,https://syntaxmem.com").split(",")
CORS(app, origins=[origin.strip() for origin in cors_origins], 
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], headers=["Content-Type", "Authorization"])

# Import utilities
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from shared.auth_middleware import verify_jwt_token_simple
from shared.database import get_forum_posts_collection, get_users_collection
from shared.utils import current_timestamp, generate_id, create_response, create_error_response

# Configure logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def validate_pagination_params(page: str, per_page: str) -> tuple[int, int]:
    """Validate and sanitize pagination parameters"""
    try:
        page_num = max(1, int(page or 1))
        per_page_num = max(1, min(50, int(per_page or 20)))  # Limit per_page to 50
        return page_num, per_page_num
    except ValueError:
        return 1, 20

def sanitize_string(text: str, max_length: int = 255) -> str:
    """Sanitize string input"""
    if not text:
        return ""
    
    # Remove HTML tags and extra whitespace
    text = re.sub(r'<[^>]+>', '', str(text))
    text = ' '.join(text.split())
    
    # Limit length
    if len(text) > max_length:
        text = text[:max_length]
    
    return text.strip()

def validate_category(category: str) -> bool:
    """Validate forum category"""
    allowed_categories = ["general", "help", "showcase", "discussion", "feedback", "announcements"]
    return category.lower() in allowed_categories


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return create_response({"status": "healthy", "service": "forum"})


@app.route("/posts", methods=["GET"])
def get_posts():
    """Get forum posts with pagination and filtering"""
    try:
        # Get query parameters
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 20)), 50)
        category = request.args.get('category')  # Optional filter
        sort_by = request.args.get('sort', 'recent')  # 'recent', 'popular', 'oldest'
        
        # Run async logic
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(_get_posts_async(page, per_page, category, sort_by))
            return create_response(result, "Forum posts retrieved")
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Error getting forum posts: {e}")
        return create_error_response("Failed to get forum posts", 500)


async def _get_posts_async(page: int, per_page: int, category: Optional[str] = None, sort_by: str = 'recent'):
    """Async logic for getting forum posts"""
    posts_collection = await get_forum_posts_collection()
    
    # Build filter
    filter_criteria = {"status": "published"}
    if category:
        filter_criteria["category"] = category
    
    # Build sort criteria
    sort_criteria = {}
    if sort_by == 'popular':
        sort_criteria = {"votes": -1, "createdAt": -1}
    elif sort_by == 'oldest':
        sort_criteria = {"createdAt": 1}
    else:  # 'recent'
        sort_criteria = {"createdAt": -1}
    
    # Calculate skip
    skip = (page - 1) * per_page
    
    # Get posts with author information
    pipeline = [
        {"$match": filter_criteria},
        {
            "$lookup": {
                "from": "users",
                "localField": "authorId",
                "foreignField": "_id",
                "as": "author"
            }
        },
        {
            "$addFields": {
                "author": {"$arrayElemAt": ["$author", 0]}
            }
        },
        {"$sort": sort_criteria},
        {"$skip": skip},
        {"$limit": per_page},
        {
            "$project": {
                "_id": 1,
                "title": 1,
                "content": 1,
                "category": 1,
                "tags": 1,
                "votes": 1,
                "replies_count": {"$size": {"$ifNull": ["$replies", []]}},
                "createdAt": 1,
                "updatedAt": 1,
                "author": {
                    "_id": "$author._id",
                    "name": "$author.name",
                    "avatar": "$author.avatar",
                    "role": "$author.role"
                }
            }
        }
    ]
    
    cursor = posts_collection.aggregate(pipeline)
    posts = await cursor.to_list(length=per_page)
    
    # Get total count
    total = await posts_collection.count_documents(filter_criteria)
    
    # Format posts
    formatted_posts = []
    for post in posts:
        formatted_posts.append({
            "id": str(post["_id"]),
            "title": post["title"],
            "content": post["content"][:200] + "..." if len(post["content"]) > 200 else post["content"],
            "category": post["category"],
            "tags": post.get("tags", []),
            "votes": post.get("votes", 0),
            "replies_count": post["replies_count"],
            "created_at": post["createdAt"],
            "updated_at": post.get("updatedAt"),
            "author": post["author"]
        })
    
    return {
        "posts": formatted_posts,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": (total + per_page - 1) // per_page
        },
        "filters": {
            "category": category,
            "sort_by": sort_by
        }
    }


@app.route("/posts", methods=["POST"])
def create_post():
    """Create a new forum post"""
    try:
        # Verify JWT token
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return create_error_response("Authorization token required", 401)
        
        token = auth_header.split(" ")[1]
        user_data = verify_jwt_token_simple(token)
        if not user_data:
            return create_error_response("Invalid or expired token", 401)
        
        user_id = user_data["user_id"]
        
        # Get request data
        data = request.get_json()
        if not data:
            return create_error_response("Invalid JSON data", 400)
        
        title = data.get("title", "").strip()
        content = data.get("content", "").strip()
        category = data.get("category", "general")
        tags = data.get("tags", [])
        
        if not title or not content:
            return create_error_response("Title and content are required", 400)
        
        if len(title) > 200:
            return create_error_response("Title too long (max 200 characters)", 400)
        
        if len(content) > 10000:
            return create_error_response("Content too long (max 10000 characters)", 400)
        
        # Run async logic
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(_create_post_async(user_id, title, content, category, tags))
            return create_response(result, "Forum post created", 201)
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Error creating forum post: {e}")
        return create_error_response("Failed to create forum post", 500)


async def _create_post_async(user_id: str, title: str, content: str, category: str, tags: List[str]):
    """Async logic for creating forum post"""
    posts_collection = await get_forum_posts_collection()
    
    # Create post
    post_id = generate_id()
    post_data = {
        "_id": post_id,
        "authorId": user_id,
        "title": title,
        "content": content,
        "category": category,
        "tags": tags[:10],  # Limit to 10 tags
        "status": "published",
        "votes": 0,
        "replies": [],
        "createdAt": current_timestamp(),
        "updatedAt": current_timestamp()
    }
    
    await posts_collection.insert_one(post_data)
    
    return {
        "post_id": post_id,
        "title": title,
        "category": category,
        "created_at": post_data["createdAt"]
    }


@app.route("/posts/<post_id>", methods=["GET"])
def get_post(post_id):
    """Get a specific forum post with replies"""
    try:
        # Run async logic
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(_get_post_async(post_id))
            return create_response(result, "Forum post retrieved")
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Error getting forum post: {e}")
        return create_error_response("Failed to get forum post", 500)


async def _get_post_async(post_id: str):
    """Async logic for getting forum post"""
    posts_collection = await get_forum_posts_collection()
    
    # Get post with author and replies
    pipeline = [
        {"$match": {"_id": post_id, "status": "published"}},
        {
            "$lookup": {
                "from": "users",
                "localField": "authorId",
                "foreignField": "_id",
                "as": "author"
            }
        },
        {
            "$lookup": {
                "from": "users",
                "localField": "replies.authorId",
                "foreignField": "_id",
                "as": "reply_authors"
            }
        },
        {
            "$addFields": {
                "author": {"$arrayElemAt": ["$author", 0]},
                "replies": {
                    "$map": {
                        "input": "$replies",
                        "as": "reply",
                        "in": {
                            "$mergeObjects": [
                                "$$reply",
                                {
                                    "author": {
                                        "$arrayElemAt": [
                                            {
                                                "$filter": {
                                                    "input": "$reply_authors",
                                                    "cond": {"$eq": ["$$this._id", "$$reply.authorId"]}
                                                }
                                            },
                                            0
                                        ]
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        },
        {
            "$project": {
                "_id": 1,
                "title": 1,
                "content": 1,
                "category": 1,
                "tags": 1,
                "votes": 1,
                "createdAt": 1,
                "updatedAt": 1,
                "author": {
                    "_id": "$author._id",
                    "name": "$author.name",
                    "avatar": "$author.avatar",
                    "role": "$author.role"
                },
                "replies": {
                    "$map": {
                        "input": "$replies",
                        "as": "reply",
                        "in": {
                            "id": "$$reply.id",
                            "content": "$$reply.content",
                            "votes": "$$reply.votes",
                            "created_at": "$$reply.createdAt",
                            "author": {
                                "_id": "$$reply.author._id",
                                "name": "$$reply.author.name",
                                "avatar": "$$reply.author.avatar",
                                "role": "$$reply.author.role"
                            }
                        }
                    }
                }
            }
        }
    ]
    
    cursor = posts_collection.aggregate(pipeline)
    posts = await cursor.to_list(length=1)
    
    if not posts:
        raise Exception("Forum post not found")
    
    post = posts[0]
    
    return {
        "id": str(post["_id"]),
        "title": post["title"],
        "content": post["content"],
        "category": post["category"],
        "tags": post.get("tags", []),
        "votes": post.get("votes", 0),
        "created_at": post["createdAt"],
        "updated_at": post.get("updatedAt"),
        "author": post["author"],
        "replies": post.get("replies", [])
    }


@app.route("/posts/<post_id>/replies", methods=["POST"])
def create_reply(post_id):
    """Create a reply to a forum post"""
    try:
        # Verify JWT token
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return create_error_response("Authorization token required", 401)
        
        token = auth_header.split(" ")[1]
        user_data = verify_jwt_token_simple(token)
        if not user_data:
            return create_error_response("Invalid or expired token", 401)
        
        user_id = user_data["user_id"]
        
        # Get request data
        data = request.get_json()
        if not data:
            return create_error_response("Invalid JSON data", 400)
        
        content = sanitize_string(data.get("content", ""), 5000)
        
        if not content:
            return create_error_response("Content is required", 400)
        
        if len(content) > 5000:
            return create_error_response("Content too long (max 5000 characters)", 400)
        
        # Run async logic
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(_create_reply_async(user_id, post_id, content))
            return create_response(result, "Reply created", 201)
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Error creating reply: {e}")
        return create_error_response("Failed to create reply", 500)


async def _create_reply_async(user_id: str, post_id: str, content: str):
    """Async logic for creating reply"""
    posts_collection = await get_forum_posts_collection()
    
    # Check if post exists
    post = await posts_collection.find_one({"_id": post_id, "status": "published"})
    if not post:
        raise Exception("Forum post not found")
    
    # Create reply
    reply_id = generate_id()
    reply_data = {
        "id": reply_id,
        "authorId": user_id,
        "content": content,
        "votes": 0,
        "createdAt": current_timestamp()
    }
    
    # Add reply to post
    await posts_collection.update_one(
        {"_id": post_id},
        {
            "$push": {"replies": reply_data},
            "$set": {"updatedAt": current_timestamp()}
        }
    )
    
    return {
        "reply_id": reply_id,
        "post_id": post_id,
        "content": content,
        "created_at": reply_data["createdAt"]
    }


@app.route("/posts/<post_id>/vote", methods=["POST"])
def vote_post(post_id):
    """Vote on a forum post"""
    try:
        # Verify JWT token
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return create_error_response("Authorization token required", 401)
        
        token = auth_header.split(" ")[1]
        user_data = verify_jwt_token_simple(token)
        if not user_data:
            return create_error_response("Invalid or expired token", 401)
        
        user_id = user_data["user_id"]
        
        # Get request data
        data = request.get_json()
        if not data:
            return create_error_response("Invalid JSON data", 400)
        
        vote_type = data.get("vote")  # 'up' or 'down'
        if vote_type not in ['up', 'down']:
            return create_error_response("Vote must be 'up' or 'down'", 400)
        
        # Run async logic
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(_vote_post_async(user_id, post_id, vote_type))
            return create_response(result, "Vote recorded")
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Error voting on post: {e}")
        return create_error_response("Failed to vote on post", 500)


async def _vote_post_async(user_id: str, post_id: str, vote_type: str):
    """Async logic for voting on post"""
    posts_collection = await get_forum_posts_collection()
    
    # Check if post exists
    post = await posts_collection.find_one({"_id": post_id, "status": "published"})
    if not post:
        raise Exception("Forum post not found")
    
    # Simple voting system - just increment/decrement
    vote_change = 1 if vote_type == 'up' else -1
    
    await posts_collection.update_one(
        {"_id": post_id},
        {
            "$inc": {"votes": vote_change},
            "$set": {"updatedAt": current_timestamp()}
        }
    )
    
    # Get updated vote count
    updated_post = await posts_collection.find_one({"_id": post_id})
    
    return {
        "post_id": post_id,
        "vote_type": vote_type,
        "new_vote_count": updated_post["votes"]
    }


@app.route("/categories", methods=["GET"])
def get_categories():
    """Get available forum categories"""
    try:
        # Run async logic
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(_get_categories_async())
            return create_response(result, "Categories retrieved")
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Error getting categories: {e}")
        return create_error_response("Failed to get categories", 500)


async def _get_categories_async():
    """Async logic for getting categories"""
    posts_collection = await get_forum_posts_collection()
    
    # Get distinct categories with post counts
    pipeline = [
        {"$match": {"status": "published"}},
        {
            "$group": {
                "_id": "$category",
                "post_count": {"$sum": 1}
            }
        },
        {"$sort": {"post_count": -1}}
    ]
    
    cursor = posts_collection.aggregate(pipeline)
    categories = await cursor.to_list(length=None)
    
    # Format categories
    formatted_categories = []
    for cat in categories:
        formatted_categories.append({
            "name": cat["_id"],
            "post_count": cat["post_count"]
        })
    
    return {
        "categories": formatted_categories
    }


@functions_framework.http
def main(request):
    """Cloud Function entry point"""
    with app.request_context(request.environ):
        return app.full_dispatch_request()