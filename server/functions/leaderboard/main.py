"""
Leaderboard Cloud Function for SyntaxMem
Handles leaderboard and user rankings using Flask
"""

import asyncio
import json
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import functions_framework
from flask import Flask, jsonify, request
from flask_cors import CORS

# Create Flask app
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://localhost:3001", "https://syntaxmem.com"], 
     methods=["GET", "POST", "OPTIONS"], headers=["Content-Type", "Authorization"])

import os
from dotenv import load_dotenv

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

# Import utilities
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))

from shared.auth_middleware import verify_jwt_token_simple
from shared.database import get_users_collection, get_practice_sessions_collection
from shared.utils import current_timestamp, create_response, create_error_response


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return create_response({"status": "healthy", "service": "leaderboard"})


@app.route("/global", methods=["GET"])
def get_global_leaderboard():
    """Get global leaderboard rankings"""
    try:
        # Get query parameters
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 50)), 100)
        language = request.args.get('language')  # Optional filter
        
        # Run async logic
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(_get_global_leaderboard_async(page, per_page, language))
            return create_response(result, "Global leaderboard retrieved")
        finally:
            loop.close()
            
    except Exception as e:
        print(f"Error getting global leaderboard: {e}")
        return create_error_response(f"Failed to get global leaderboard: {str(e)}", 500)


async def _get_global_leaderboard_async(page: int, per_page: int, language: Optional[str] = None):
    """Async logic for getting global leaderboard"""
    users_collection = await get_users_collection()
    practice_collection = await get_practice_sessions_collection()
    
    # Calculate skip
    skip = (page - 1) * per_page
    
    # Build aggregation pipeline for language-specific leaderboard
    if language:
        # Get top users by total score in specific language
        pipeline = [
            {
                "$lookup": {
                    "from": "practice_sessions",
                    "let": {"user_id": "$_id"},
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {"$eq": ["$userId", "$$user_id"]},
                                "status": "completed"
                            }
                        },
                        {
                            "$lookup": {
                                "from": "snippets",
                                "localField": "snippetId",
                                "foreignField": "_id",
                                "as": "snippet"
                            }
                        },
                        {
                            "$match": {
                                "snippet.language": language
                            }
                        },
                        {
                            "$group": {
                                "_id": None,
                                "totalScore": {"$sum": "$score"},
                                "totalTime": {"$sum": "$timeSpent"},
                                "sessionsCount": {"$sum": 1}
                            }
                        }
                    ],
                    "as": "language_stats"
                }
            },
            {
                "$match": {
                    "language_stats": {"$ne": []}
                }
            },
            {
                "$addFields": {
                    "language_total_score": {"$arrayElemAt": ["$language_stats.totalScore", 0]},
                    "language_total_time": {"$arrayElemAt": ["$language_stats.totalTime", 0]},
                    "language_sessions": {"$arrayElemAt": ["$language_stats.sessionsCount", 0]}
                }
            },
            {
                "$sort": {"language_total_score": -1, "language_total_time": 1}
            },
            {
                "$skip": skip
            },
            {
                "$limit": per_page
            },
            {
                "$project": {
                    "name": 1,
                    "avatar": 1,
                    "total_score": "$language_total_score",
                    "total_time": "$language_total_time",
                    "sessions_count": "$language_sessions",
                    "level": "$stats.level"
                }
            }
        ]
    else:
        # Global leaderboard by total score
        pipeline = [
            {
                "$sort": {"stats.totalScore": -1, "stats.practiceTime": 1}
            },
            {
                "$skip": skip
            },
            {
                "$limit": per_page
            },
            {
                "$project": {
                    "name": 1,
                    "avatar": 1,
                    "total_score": "$stats.totalScore",
                    "total_time": "$stats.practiceTime",
                    "level": "$stats.level",
                    "streak": "$stats.streak"
                }
            }
        ]
    
    # Execute aggregation
    cursor = users_collection.aggregate(pipeline)
    users = await cursor.to_list(length=per_page)
    
    # Get total count for pagination
    if language:
        # Count users with sessions in specific language
        count_pipeline = [
            {
                "$lookup": {
                    "from": "practice_sessions",
                    "let": {"user_id": "$_id"},
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {"$eq": ["$userId", "$$user_id"]},
                                "status": "completed"
                            }
                        },
                        {
                            "$lookup": {
                                "from": "snippets",
                                "localField": "snippetId",
                                "foreignField": "_id",
                                "as": "snippet"
                            }
                        },
                        {
                            "$match": {
                                "snippet.language": language
                            }
                        }
                    ],
                    "as": "language_sessions"
                }
            },
            {
                "$match": {
                    "language_sessions": {"$ne": []}
                }
            },
            {
                "$count": "total"
            }
        ]
        count_result = await users_collection.aggregate(count_pipeline).to_list(length=1)
        total = count_result[0]["total"] if count_result else 0
    else:
        total = await users_collection.count_documents({})
    
    # Add rankings
    ranked_users = []
    for i, user in enumerate(users):
        ranked_users.append({
            "rank": skip + i + 1,
            "user_id": str(user["_id"]),
            "name": user["name"],
            "avatar": user["avatar"],
            "total_score": user["total_score"],
            "total_time": user.get("total_time", 0),
            "level": user.get("level", 1),
            "streak": user.get("streak", 0),
            "sessions_count": user.get("sessions_count")
        })
    
    return {
        "leaderboard": ranked_users,
        "language": language,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": (total + per_page - 1) // per_page
        }
    }


@app.route("/weekly", methods=["GET"])
def get_weekly_leaderboard():
    """Get weekly leaderboard rankings"""
    try:
        # Get query parameters
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 50)), 100)
        language = request.args.get('language')  # Optional filter
        
        # Run async logic
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(_get_weekly_leaderboard_async(page, per_page, language))
            return create_response(result, "Weekly leaderboard retrieved")
        finally:
            loop.close()
            
    except Exception as e:
        print(f"Error getting weekly leaderboard: {e}")
        return create_error_response(f"Failed to get weekly leaderboard: {str(e)}", 500)


async def _get_weekly_leaderboard_async(page: int, per_page: int, language: Optional[str] = None):
    """Async logic for getting weekly leaderboard"""
    users_collection = await get_users_collection()
    practice_collection = await get_practice_sessions_collection()
    
    # Calculate skip
    skip = (page - 1) * per_page
    
    # Get start of current week (Monday)
    now = datetime.now(timezone.utc)
    days_since_monday = now.weekday()
    week_start = now - timedelta(days=days_since_monday, hours=now.hour, 
                                minutes=now.minute, seconds=now.second, 
                                microseconds=now.microsecond)
    
    # Build match criteria for this week
    week_match = {
        "completedAt": {"$gte": week_start},
        "status": "completed"
    }
    
    if language:
        # Weekly leaderboard for specific language
        pipeline = [
            {
                "$lookup": {
                    "from": "practice_sessions",
                    "let": {"user_id": "$_id"},
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {"$eq": ["$userId", "$$user_id"]},
                                **week_match
                            }
                        },
                        {
                            "$lookup": {
                                "from": "snippets",
                                "localField": "snippetId",
                                "foreignField": "_id",
                                "as": "snippet"
                            }
                        },
                        {
                            "$match": {
                                "snippet.language": language
                            }
                        },
                        {
                            "$group": {
                                "_id": None,
                                "weeklyScore": {"$sum": "$score"},
                                "weeklyTime": {"$sum": "$timeSpent"},
                                "weeklySessions": {"$sum": 1}
                            }
                        }
                    ],
                    "as": "weekly_stats"
                }
            },
            {
                "$match": {
                    "weekly_stats": {"$ne": []}
                }
            },
            {
                "$addFields": {
                    "weekly_score": {"$arrayElemAt": ["$weekly_stats.weeklyScore", 0]},
                    "weekly_time": {"$arrayElemAt": ["$weekly_stats.weeklyTime", 0]},
                    "weekly_sessions": {"$arrayElemAt": ["$weekly_stats.weeklySessions", 0]}
                }
            }
        ]
    else:
        # Global weekly leaderboard
        pipeline = [
            {
                "$lookup": {
                    "from": "practice_sessions",
                    "let": {"user_id": "$_id"},
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {"$eq": ["$userId", "$$user_id"]},
                                **week_match
                            }
                        },
                        {
                            "$group": {
                                "_id": None,
                                "weeklyScore": {"$sum": "$score"},
                                "weeklyTime": {"$sum": "$timeSpent"},
                                "weeklySessions": {"$sum": 1}
                            }
                        }
                    ],
                    "as": "weekly_stats"
                }
            },
            {
                "$match": {
                    "weekly_stats": {"$ne": []}
                }
            },
            {
                "$addFields": {
                    "weekly_score": {"$arrayElemAt": ["$weekly_stats.weeklyScore", 0]},
                    "weekly_time": {"$arrayElemAt": ["$weekly_stats.weeklyTime", 0]},
                    "weekly_sessions": {"$arrayElemAt": ["$weekly_stats.weeklySessions", 0]}
                }
            }
        ]
    
    # Add sorting and pagination
    pipeline.extend([
        {
            "$sort": {"weekly_score": -1, "weekly_time": 1}
        },
        {
            "$skip": skip
        },
        {
            "$limit": per_page
        },
        {
            "$project": {
                "name": 1,
                "avatar": 1,
                "weekly_score": 1,
                "weekly_time": 1,
                "weekly_sessions": 1,
                "level": "$stats.level"
            }
        }
    ])
    
    # Execute aggregation
    cursor = users_collection.aggregate(pipeline)
    users = await cursor.to_list(length=per_page)
    
    # Add rankings
    ranked_users = []
    for i, user in enumerate(users):
        ranked_users.append({
            "rank": skip + i + 1,
            "user_id": str(user["_id"]),
            "name": user["name"],
            "avatar": user["avatar"],
            "weekly_score": user["weekly_score"],
            "weekly_time": user["weekly_time"],
            "weekly_sessions": user["weekly_sessions"],
            "level": user.get("level", 1)
        })
    
    return {
        "leaderboard": ranked_users,
        "language": language,
        "week_start": week_start.isoformat(),
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": len(ranked_users),  # Simplified for weekly
            "pages": 1  # Simplified for weekly
        }
    }


@app.route("/user/<user_id>/rank", methods=["GET"])
def get_user_rank(user_id):
    """Get specific user's rank and stats"""
    try:
        # Get query parameters
        language = request.args.get('language')  # Optional filter
        timeframe = request.args.get('timeframe', 'all')  # 'all', 'weekly'
        
        # Run async logic
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(_get_user_rank_async(user_id, language, timeframe))
            return create_response(result, "User rank retrieved")
        finally:
            loop.close()
            
    except Exception as e:
        print(f"Error getting user rank: {e}")
        return create_error_response(f"Failed to get user rank: {str(e)}", 500)


async def _get_user_rank_async(user_id: str, language: Optional[str] = None, timeframe: str = 'all'):
    """Async logic for getting user rank"""
    users_collection = await get_users_collection()
    practice_collection = await get_practice_sessions_collection()
    
    # Get user data
    user = await users_collection.find_one({"_id": user_id})
    if not user:
        raise Exception("User not found")
    
    # Build time filter for weekly
    time_filter = {}
    if timeframe == 'weekly':
        now = datetime.now(timezone.utc)
        days_since_monday = now.weekday()
        week_start = now - timedelta(days=days_since_monday, hours=now.hour, 
                                    minutes=now.minute, seconds=now.second, 
                                    microseconds=now.microsecond)
        time_filter["completedAt"] = {"$gte": week_start}
    
    # Get user's score and calculate rank
    if language:
        # Language-specific rank
        user_sessions = await practice_collection.aggregate([
            {
                "$match": {
                    "userId": user_id,
                    "status": "completed",
                    **time_filter
                }
            },
            {
                "$lookup": {
                    "from": "snippets",
                    "localField": "snippetId",
                    "foreignField": "_id",
                    "as": "snippet"
                }
            },
            {
                "$match": {
                    "snippet.language": language
                }
            },
            {
                "$group": {
                    "_id": None,
                    "totalScore": {"$sum": "$score"},
                    "totalTime": {"$sum": "$timeSpent"},
                    "sessionsCount": {"$sum": 1}
                }
            }
        ]).to_list(length=1)
        
        user_score = user_sessions[0]["totalScore"] if user_sessions else 0
        user_time = user_sessions[0]["totalTime"] if user_sessions else 0
        user_sessions_count = user_sessions[0]["sessionsCount"] if user_sessions else 0
    else:
        # Global rank
        if timeframe == 'weekly':
            user_sessions = await practice_collection.aggregate([
                {
                    "$match": {
                        "userId": user_id,
                        "status": "completed",
                        **time_filter
                    }
                },
                {
                    "$group": {
                        "_id": None,
                        "totalScore": {"$sum": "$score"},
                        "totalTime": {"$sum": "$timeSpent"},
                        "sessionsCount": {"$sum": 1}
                    }
                }
            ]).to_list(length=1)
            
            user_score = user_sessions[0]["totalScore"] if user_sessions else 0
            user_time = user_sessions[0]["totalTime"] if user_sessions else 0
            user_sessions_count = user_sessions[0]["sessionsCount"] if user_sessions else 0
        else:
            user_score = user["stats"]["totalScore"]
            user_time = user["stats"]["practiceTime"]
            user_sessions_count = await practice_collection.count_documents({
                "userId": user_id,
                "status": "completed"
            })
    
    # Calculate rank by counting users with higher scores
    if language:
        higher_users = await users_collection.aggregate([
            {
                "$lookup": {
                    "from": "practice_sessions",
                    "let": {"user_id": "$_id"},
                    "pipeline": [
                        {
                            "$match": {
                                "$expr": {"$eq": ["$userId", "$$user_id"]},
                                "status": "completed",
                                **time_filter
                            }
                        },
                        {
                            "$lookup": {
                                "from": "snippets",
                                "localField": "snippetId",
                                "foreignField": "_id",
                                "as": "snippet"
                            }
                        },
                        {
                            "$match": {
                                "snippet.language": language
                            }
                        },
                        {
                            "$group": {
                                "_id": None,
                                "totalScore": {"$sum": "$score"}
                            }
                        }
                    ],
                    "as": "language_stats"
                }
            },
            {
                "$match": {
                    "language_stats.totalScore": {"$gt": user_score}
                }
            },
            {
                "$count": "count"
            }
        ]).to_list(length=1)
    else:
        if timeframe == 'weekly':
            higher_users = await users_collection.aggregate([
                {
                    "$lookup": {
                        "from": "practice_sessions",
                        "let": {"user_id": "$_id"},
                        "pipeline": [
                            {
                                "$match": {
                                    "$expr": {"$eq": ["$userId", "$$user_id"]},
                                    "status": "completed",
                                    **time_filter
                                }
                            },
                            {
                                "$group": {
                                    "_id": None,
                                    "totalScore": {"$sum": "$score"}
                                }
                            }
                        ],
                        "as": "weekly_stats"
                    }
                },
                {
                    "$match": {
                        "weekly_stats.totalScore": {"$gt": user_score}
                    }
                },
                {
                    "$count": "count"
                }
            ]).to_list(length=1)
        else:
            higher_users = await users_collection.count_documents({
                "stats.totalScore": {"$gt": user_score}
            })
            higher_users = [{"count": higher_users}]
    
    rank = (higher_users[0]["count"] if higher_users else 0) + 1
    
    return {
        "user_id": user_id,
        "name": user["name"],
        "avatar": user["avatar"],
        "rank": rank,
        "score": user_score,
        "time": user_time,
        "sessions_count": user_sessions_count,
        "level": user["stats"]["level"],
        "language": language,
        "timeframe": timeframe
    }


@functions_framework.http
def main(request):
    """Cloud Function entry point"""
    with app.request_context(request.environ):
        return app.full_dispatch_request()