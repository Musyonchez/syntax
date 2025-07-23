"""
Leaderboard Cloud Function for SyntaxMem
Handles leaderboard rankings, filtering, and user achievements
"""
import functions_framework
from fastapi import FastAPI, HTTPException, status, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from bson import ObjectId
import sys
import os
from a2wsgi import ASGIMiddleware


# Add shared modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from shared.database import (
    get_leaderboard_collection,
    get_users_collection,
    get_snippets_collection,
    get_practice_sessions_collection
)
from shared.auth_middleware import verify_token, optional_auth
from shared.cors_handler import handle_cors_request
from shared.utils import (
    current_timestamp, create_response, create_error_response,
    paginate_results, normalize_language, validate_language
)

app = FastAPI(title="SyntaxMem Leaderboard Service")

# Import configuration
from shared.config import config

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Response models
class LeaderboardEntry(BaseModel):
    """Leaderboard entry model"""
    rank: int
    user_id: str
    user_name: str
    user_avatar: Optional[str]
    score: int
    accuracy: float
    difficulty: int
    time_spent: float
    snippet_count: int
    date_submitted: str
    is_current_user: bool = False


class LeaderboardResponse(BaseModel):
    """Leaderboard response model"""
    entries: List[LeaderboardEntry]
    current_user_rank: Optional[int]
    total_entries: int
    language: str
    time_period: str
    pagination: Dict[str, Any]


class UserRankingResponse(BaseModel):
    """User ranking response"""
    user_id: str
    global_rank: Optional[int]
    language_ranks: Dict[str, int]
    total_score: int
    best_accuracy: float
    total_snippets_solved: int
    practice_time: float
    achievements: List[str]


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return create_response({"status": "healthy", "service": "leaderboard"})


@app.get("/", response_model=LeaderboardResponse)
async def get_leaderboard(
    language: str = Query("all", description="Language filter (python, javascript, all)"),
    time_period: str = Query("all", description="Time period (today, week, month, all)"),
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    user_data: Optional[Dict[str, Any]] = Depends(optional_auth)
):
    """
    Get leaderboard with filtering and pagination
    """
    try:
        leaderboard_collection = await get_leaderboard_collection()
        users_collection = await get_users_collection()
        
        # Build query
        query = {}
        
        # Language filter
        if language != "all":
            if not validate_language(language):
                raise HTTPException(status_code=400, detail="Invalid language")
            query["leaderboard_type"] = normalize_language(language)
        
        # Time period filter
        now = current_timestamp()
        if time_period == "today":
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            query["dateOfSubmission"] = {"$gte": start_date}
        elif time_period == "week":
            start_date = now - timedelta(days=7)
            query["dateOfSubmission"] = {"$gte": start_date}
        elif time_period == "month":
            start_date = now - timedelta(days=30)
            query["dateOfSubmission"] = {"$gte": start_date}
        
        # Aggregate leaderboard data
        pipeline = [
            {"$match": query},
            {
                "$group": {
                    "_id": {
                        "userId": "$userId",
                        "userName": "$userName"
                    },
                    "totalScore": {"$sum": "$score"},
                    "avgAccuracy": {"$avg": "$similarity"},
                    "avgDifficulty": {"$avg": "$difficulty"},
                    "totalTime": {"$sum": "$timeSpent"},
                    "snippetCount": {"$sum": 1},
                    "lastSubmission": {"$max": "$dateOfSubmission"},
                    "bestScore": {"$max": "$score"}
                }
            },
            {
                "$sort": {
                    "totalScore": -1,
                    "avgAccuracy": -1,
                    "lastSubmission": -1
                }
            }
        ]
        
        # Get aggregated results
        leaderboard_data = await leaderboard_collection.aggregate(pipeline).to_list(None)
        total_entries = len(leaderboard_data)
        
        # Calculate pagination
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_data = leaderboard_data[start_idx:end_idx]
        
        # Get user avatars
        user_ids = [entry["_id"]["userId"] for entry in paginated_data]
        users = await users_collection.find(
            {"_id": {"$in": user_ids}},
            {"avatar": 1}
        ).to_list(None)
        user_avatars = {str(user["_id"]): user.get("avatar", "") for user in users}
        
        # Format leaderboard entries
        entries = []
        current_user_rank = None
        current_user_id = user_data["user_id"] if user_data else None
        
        for idx, entry in enumerate(paginated_data):
            rank = start_idx + idx + 1
            user_id = entry["_id"]["userId"]
            
            leaderboard_entry = LeaderboardEntry(
                rank=rank,
                user_id=user_id,
                user_name=entry["_id"]["userName"],
                user_avatar=user_avatars.get(user_id, ""),
                score=int(entry["totalScore"]),
                accuracy=round(entry["avgAccuracy"], 3),
                difficulty=round(entry["avgDifficulty"], 1),
                time_spent=round(entry["totalTime"], 1),
                snippet_count=entry["snippetCount"],
                date_submitted=entry["lastSubmission"].isoformat(),
                is_current_user=(user_id == current_user_id)
            )
            
            entries.append(leaderboard_entry)
            
            # Track current user's rank
            if user_id == current_user_id:
                current_user_rank = rank
        
        # If current user not in current page, find their rank
        if current_user_id and current_user_rank is None:
            for idx, entry in enumerate(leaderboard_data):
                if entry["_id"]["userId"] == current_user_id:
                    current_user_rank = idx + 1
                    break
        
        # Calculate pagination info
        total_pages = (total_entries + per_page - 1) // per_page
        
        return LeaderboardResponse(
            entries=entries,
            current_user_rank=current_user_rank,
            total_entries=total_entries,
            language=language,
            time_period=time_period,
            pagination={
                "page": page,
                "per_page": per_page,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_prev": page > 1
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get leaderboard: {str(e)}"
        )


@app.get("/user/{user_id}", response_model=UserRankingResponse)
async def get_user_ranking(
    user_id: str,
    current_user: Optional[Dict[str, Any]] = Depends(optional_auth)
):
    """
    Get specific user's ranking and achievements
    """
    try:
        leaderboard_collection = await get_leaderboard_collection()
        users_collection = await get_users_collection()
        practice_sessions_collection = await get_practice_sessions_collection()
        
        # Validate user exists
        user = await users_collection.find_one({"_id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get user's leaderboard entries
        user_entries = await leaderboard_collection.find({"userId": user_id}).to_list(None)
        
        if not user_entries:
            # User has no leaderboard entries yet
            return UserRankingResponse(
                user_id=user_id,
                global_rank=None,
                language_ranks={},
                total_score=0,
                best_accuracy=0.0,
                total_snippets_solved=0,
                practice_time=0.0,
                achievements=user.get("stats", {}).get("achievements", [])
            )
        
        # Calculate user statistics
        total_score = sum(entry["score"] for entry in user_entries)
        best_accuracy = max(entry["similarity"] for entry in user_entries)
        total_snippets = len(user_entries)
        total_time = sum(entry.get("timeSpent", 0) for entry in user_entries)
        
        # Calculate global rank
        global_pipeline = [
            {
                "$group": {
                    "_id": "$userId",
                    "totalScore": {"$sum": "$score"}
                }
            },
            {"$sort": {"totalScore": -1}}
        ]
        
        global_rankings = await leaderboard_collection.aggregate(global_pipeline).to_list(None)
        global_rank = None
        for idx, ranking in enumerate(global_rankings):
            if ranking["_id"] == user_id:
                global_rank = idx + 1
                break
        
        # Calculate language-specific ranks
        language_ranks = {}
        for language in ["python", "javascript"]:
            lang_pipeline = [
                {"$match": {"leaderboard_type": language}},
                {
                    "$group": {
                        "_id": "$userId",
                        "totalScore": {"$sum": "$score"}
                    }
                },
                {"$sort": {"totalScore": -1}}
            ]
            
            lang_rankings = await leaderboard_collection.aggregate(lang_pipeline).to_list(None)
            for idx, ranking in enumerate(lang_rankings):
                if ranking["_id"] == user_id:
                    language_ranks[language] = idx + 1
                    break
        
        return UserRankingResponse(
            user_id=user_id,
            global_rank=global_rank,
            language_ranks=language_ranks,
            total_score=total_score,
            best_accuracy=round(best_accuracy, 3),
            total_snippets_solved=total_snippets,
            practice_time=round(total_time, 1),
            achievements=user.get("stats", {}).get("achievements", [])
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user ranking: {str(e)}"
        )


@app.get("/my-ranking", response_model=UserRankingResponse)
async def get_my_ranking(
    user_data: Dict[str, Any] = Depends(verify_token)
):
    """
    Get current user's ranking and achievements
    """
    return await get_user_ranking(user_data["user_id"], user_data)


@app.get("/stats")
async def get_leaderboard_stats(
    user_data: Optional[Dict[str, Any]] = Depends(optional_auth)
):
    """
    Get overall leaderboard statistics
    """
    try:
        leaderboard_collection = await get_leaderboard_collection()
        users_collection = await get_users_collection()
        
        # Overall statistics
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "totalEntries": {"$sum": 1},
                    "avgScore": {"$avg": "$score"},
                    "maxScore": {"$max": "$score"},
                    "avgAccuracy": {"$avg": "$similarity"},
                    "totalPracticeTime": {"$sum": "$timeSpent"}
                }
            }
        ]
        
        overall_stats = await leaderboard_collection.aggregate(pipeline).to_list(1)
        stats = overall_stats[0] if overall_stats else {}
        
        # Language breakdown
        language_pipeline = [
            {
                "$group": {
                    "_id": "$leaderboard_type",
                    "entries": {"$sum": 1},
                    "avgScore": {"$avg": "$score"},
                    "maxScore": {"$max": "$score"}
                }
            }
        ]
        
        language_stats = await leaderboard_collection.aggregate(language_pipeline).to_list(None)
        
        # Active users count
        active_users = await leaderboard_collection.distinct("userId")
        
        # Recent activity (last 7 days)
        week_ago = current_timestamp() - timedelta(days=7)
        recent_entries = await leaderboard_collection.count_documents({
            "dateOfSubmission": {"$gte": week_ago}
        })
        
        return create_response({
            "total_entries": stats.get("totalEntries", 0),
            "active_users": len(active_users),
            "average_score": round(stats.get("avgScore", 0), 2),
            "highest_score": stats.get("maxScore", 0),
            "average_accuracy": round(stats.get("avgAccuracy", 0), 3),
            "total_practice_hours": round(stats.get("totalPracticeTime", 0) / 3600, 1),
            "recent_activity": recent_entries,
            "languages": {
                lang["_id"]: {
                    "entries": lang["entries"],
                    "avg_score": round(lang["avgScore"], 2),
                    "max_score": lang["maxScore"]
                }
                for lang in language_stats
            }
        })
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get leaderboard stats: {str(e)}"
        )


@app.get("/top-performers")
async def get_top_performers(
    language: str = Query("all"),
    limit: int = Query(10, ge=1, le=50)
):
    """
    Get top performers across different categories
    """
    try:
        leaderboard_collection = await get_leaderboard_collection()
        users_collection = await get_users_collection()
        
        # Build base query
        base_query = {}
        if language != "all":
            if not validate_language(language):
                raise HTTPException(status_code=400, detail="Invalid language")
            base_query["leaderboard_type"] = normalize_language(language)
        
        # Top by total score
        score_pipeline = [
            {"$match": base_query},
            {
                "$group": {
                    "_id": {
                        "userId": "$userId",
                        "userName": "$userName"
                    },
                    "totalScore": {"$sum": "$score"},
                    "snippetCount": {"$sum": 1}
                }
            },
            {"$sort": {"totalScore": -1}},
            {"$limit": limit}
        ]
        
        # Top by accuracy
        accuracy_pipeline = [
            {"$match": base_query},
            {
                "$group": {
                    "_id": {
                        "userId": "$userId",
                        "userName": "$userName"
                    },
                    "avgAccuracy": {"$avg": "$similarity"},
                    "snippetCount": {"$sum": 1}
                }
            },
            {"$match": {"snippetCount": {"$gte": 5}}},  # Minimum 5 snippets for accuracy ranking
            {"$sort": {"avgAccuracy": -1}},
            {"$limit": limit}
        ]
        
        # Top by speed (lowest average time)
        speed_pipeline = [
            {"$match": {**base_query, "timeSpent": {"$gt": 0}}},
            {
                "$group": {
                    "_id": {
                        "userId": "$userId",
                        "userName": "$userName"
                    },
                    "avgTime": {"$avg": "$timeSpent"},
                    "snippetCount": {"$sum": 1}
                }
            },
            {"$match": {"snippetCount": {"$gte": 5}}},  # Minimum 5 snippets for speed ranking
            {"$sort": {"avgTime": 1}},
            {"$limit": limit}
        ]
        
        # Execute all pipelines
        top_scores = await leaderboard_collection.aggregate(score_pipeline).to_list(None)
        top_accuracy = await leaderboard_collection.aggregate(accuracy_pipeline).to_list(None)
        top_speed = await leaderboard_collection.aggregate(speed_pipeline).to_list(None)
        
        # Get user avatars
        all_user_ids = set()
        for category in [top_scores, top_accuracy, top_speed]:
            all_user_ids.update(entry["_id"]["userId"] for entry in category)
        
        users = await users_collection.find(
            {"_id": {"$in": list(all_user_ids)}},
            {"avatar": 1}
        ).to_list(None)
        user_avatars = {str(user["_id"]): user.get("avatar", "") for user in users}
        
        # Format results
        def format_performer(entry, rank, metric_key, metric_value):
            user_id = entry["_id"]["userId"]
            return {
                "rank": rank,
                "user_id": user_id,
                "user_name": entry["_id"]["userName"],
                "user_avatar": user_avatars.get(user_id, ""),
                "snippet_count": entry["snippetCount"],
                metric_key: metric_value
            }
        
        formatted_top_scores = [
            format_performer(entry, idx + 1, "total_score", entry["totalScore"])
            for idx, entry in enumerate(top_scores)
        ]
        
        formatted_top_accuracy = [
            format_performer(entry, idx + 1, "accuracy", round(entry["avgAccuracy"], 3))
            for idx, entry in enumerate(top_accuracy)
        ]
        
        formatted_top_speed = [
            format_performer(entry, idx + 1, "avg_time", round(entry["avgTime"], 1))
            for idx, entry in enumerate(top_speed)
        ]
        
        return create_response({
            "top_scores": formatted_top_scores,
            "top_accuracy": formatted_top_accuracy,
            "top_speed": formatted_top_speed,
            "language": language,
            "limit": limit
        })
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get top performers: {str(e)}"
        )


@app.post("/recalculate-ranks")
async def recalculate_ranks(
    admin_data: Dict[str, Any] = Depends(verify_token)
):
    """
    Recalculate all leaderboard ranks (admin function)
    Note: This is a maintenance function that can be called periodically
    """
    try:
        # Only allow admin users (for now, any authenticated user can trigger this)
        # In production, you might want to add admin verification
        
        leaderboard_collection = await get_leaderboard_collection()
        
        # Get all languages
        languages = await leaderboard_collection.distinct("leaderboard_type")
        
        updated_count = 0
        
        for language in languages:
            # Get sorted leaderboard for this language
            pipeline = [
                {"$match": {"leaderboard_type": language}},
                {
                    "$group": {
                        "_id": "$userId",
                        "totalScore": {"$sum": "$score"},
                        "entries": {"$push": "$ROOT"}
                    }
                },
                {"$sort": {"totalScore": -1}}
            ]
            
            ranked_users = await leaderboard_collection.aggregate(pipeline).to_list(None)
            
            # Update ranks for each user's entries
            for rank, user_data in enumerate(ranked_users, 1):
                user_id = user_data["_id"]
                entry_ids = [entry["_id"] for entry in user_data["entries"]]
                
                # Update all entries for this user in this language
                await leaderboard_collection.update_many(
                    {"_id": {"$in": entry_ids}},
                    {"$set": {"rank": rank}}
                )
                
                updated_count += len(entry_ids)
        
        return create_response({
            "message": "Ranks recalculated successfully",
            "updated_entries": updated_count,
            "languages_processed": len(languages)
        })
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to recalculate ranks: {str(e)}"
        )


@functions_framework.http
def main(request):
    """Cloud Function entry point"""
    return handle_cors_request(app, request)