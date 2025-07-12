"""
Practice Session Cloud Function for SyntaxMem
Handles practice attempts, scoring, and progress tracking
"""
import functions_framework
from fastapi import FastAPI, HTTPException, status, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from bson import ObjectId
import sys
import os

# Add shared modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from shared.database import (
    get_snippets_collection, 
    get_users_collection,
    get_practice_sessions_collection,
    get_leaderboard_collection
)
from shared.auth_middleware import verify_token
from shared.masking import mask_code, calculate_score, validate_answer
from shared.utils import (
    generate_id, current_timestamp, create_response, create_error_response,
    clean_user_input, Timer
)

app = FastAPI(title="SyntaxMem Practice Service")

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


# Request/Response models
class StartPracticeRequest(BaseModel):
    """Start practice session request"""
    snippet_id: str
    difficulty: Optional[int] = Field(None, ge=1, le=10)


class SubmitPracticeRequest(BaseModel):
    """Submit practice attempt request"""
    session_id: str
    user_answers: List[str]
    time_taken: float = Field(..., ge=0, le=3600)  # Max 1 hour


class PracticeSessionResponse(BaseModel):
    """Practice session response"""
    session_id: str
    snippet_id: str
    snippet_title: str
    language: str
    difficulty: int
    masked_code: str
    answer_count: int
    max_time: int
    created_at: str


class ScoreResponse(BaseModel):
    """Score response"""
    session_id: str
    total_score: float
    accuracy: float
    time_bonus: float
    mistakes: int
    time_taken: float
    detailed_results: List[Dict[str, Any]]
    leaderboard_eligible: bool


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return create_response({"status": "healthy", "service": "practice"})


@app.post("/start", response_model=PracticeSessionResponse)
async def start_practice_session(
    request: StartPracticeRequest,
    user_data: Dict[str, Any] = Depends(verify_token)
):
    """
    Start a new practice session with masked code
    """
    try:
        snippets_collection = await get_snippets_collection()
        practice_sessions_collection = await get_practice_sessions_collection()
        
        # Validate snippet ID
        try:
            ObjectId(request.snippet_id)
        except:
            raise HTTPException(status_code=400, detail="Invalid snippet ID")
        
        # Get snippet
        snippet = await snippets_collection.find_one({"_id": request.snippet_id})
        
        if not snippet:
            raise HTTPException(status_code=404, detail="Snippet not found")
        
        # Check permissions
        user_id = user_data["user_id"]
        if snippet["type"] == "personal" and snippet["author"] != user_id:
            raise HTTPException(status_code=403, detail="Access denied")
        elif snippet["type"] == "official" and snippet["status"] != "active":
            raise HTTPException(status_code=403, detail="Snippet not available for practice")
        
        # Use custom difficulty or snippet's default
        difficulty = request.difficulty or snippet["difficulty"]
        
        # Generate masked code
        masked_code, correct_answers = mask_code(
            snippet["content"],
            snippet["language"],
            difficulty
        )
        
        # Create practice session
        session_id = generate_id()
        session = {
            "_id": session_id,
            "userId": user_id,
            "snippetId": request.snippet_id,
            "snippetType": snippet["type"],
            "language": snippet["language"],
            "difficulty": difficulty,
            "maskedCode": masked_code,
            "correctAnswers": correct_answers,
            "userAnswers": [],
            "completed": False,
            "score": None,
            "timeSpent": 0,
            "mistakes": [],
            "createdAt": current_timestamp(),
            "completedAt": None
        }
        
        await practice_sessions_collection.insert_one(session)
        
        return PracticeSessionResponse(
            session_id=session_id,
            snippet_id=request.snippet_id,
            snippet_title=snippet["title"],
            language=snippet["language"],
            difficulty=difficulty,
            masked_code=masked_code,
            answer_count=len(correct_answers),
            max_time=300,  # 5 minutes default
            created_at=session["createdAt"].isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start practice session: {str(e)}"
        )


@app.post("/submit", response_model=ScoreResponse)
async def submit_practice_attempt(
    request: SubmitPracticeRequest,
    user_data: Dict[str, Any] = Depends(verify_token)
):
    """
    Submit practice attempt and calculate score
    """
    try:
        practice_sessions_collection = await get_practice_sessions_collection()
        snippets_collection = await get_snippets_collection()
        users_collection = await get_users_collection()
        
        # Validate session ID
        try:
            ObjectId(request.session_id)
        except:
            raise HTTPException(status_code=400, detail="Invalid session ID")
        
        # Get practice session
        session = await practice_sessions_collection.find_one({"_id": request.session_id})
        
        if not session:
            raise HTTPException(status_code=404, detail="Practice session not found")
        
        # Verify ownership
        user_id = user_data["user_id"]
        if session["userId"] != user_id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Check if already completed
        if session["completed"]:
            raise HTTPException(status_code=400, detail="Session already completed")
        
        # Validate answers count
        correct_answers = session["correctAnswers"]
        if len(request.user_answers) != len(correct_answers):
            raise HTTPException(
                status_code=400, 
                detail=f"Expected {len(correct_answers)} answers, got {len(request.user_answers)}"
            )
        
        # Calculate detailed results
        detailed_results = []
        mistakes = []
        
        for i, (user_answer, correct_answer) in enumerate(zip(request.user_answers, correct_answers)):
            similarity = validate_answer(user_answer, correct_answer)
            is_correct = similarity >= 0.8  # 80% similarity threshold
            
            result = {
                "position": i,
                "user_answer": user_answer,
                "correct_answer": correct_answer,
                "similarity": similarity,
                "is_correct": is_correct
            }
            detailed_results.append(result)
            
            if not is_correct:
                mistakes.append({
                    "position": i,
                    "expected": correct_answer,
                    "provided": user_answer,
                    "similarity": similarity
                })
        
        # Calculate overall score
        score_data = calculate_score(
            request.user_answers,
            correct_answers,
            request.time_taken,
            max_time=300
        )
        
        # Update practice session
        completion_time = current_timestamp()
        await practice_sessions_collection.update_one(
            {"_id": request.session_id},
            {
                "$set": {
                    "userAnswers": request.user_answers,
                    "completed": True,
                    "score": score_data,
                    "timeSpent": request.time_taken,
                    "mistakes": mistakes,
                    "completedAt": completion_time
                }
            }
        )
        
        # Get snippet info
        snippet = await snippets_collection.find_one({"_id": session["snippetId"]})
        
        # Update snippet solve count and average score
        if snippet:
            new_solve_count = snippet.get("solveCount", 0) + 1
            current_avg = snippet.get("avgScore", 0.0)
            new_avg = ((current_avg * (new_solve_count - 1)) + score_data["total_score"]) / new_solve_count
            
            await snippets_collection.update_one(
                {"_id": session["snippetId"]},
                {
                    "$set": {
                        "solveCount": new_solve_count,
                        "avgScore": round(new_avg, 2)
                    }
                }
            )
        
        # Update user stats
        user = user_data["user"]
        current_stats = user.get("stats", {})
        new_total_score = current_stats.get("totalScore", 0) + score_data["total_score"]
        new_practice_time = current_stats.get("practiceTime", 0) + request.time_taken
        
        await users_collection.update_one(
            {"_id": user_id},
            {
                "$set": {
                    "stats.totalScore": new_total_score,
                    "stats.practiceTime": new_practice_time,
                    "lastActive": completion_time
                }
            }
        )
        
        # Add to leaderboard if official snippet
        leaderboard_eligible = snippet and snippet["type"] == "official"
        
        if leaderboard_eligible:
            await self._add_to_leaderboard(
                user_id=user_id,
                snippet_id=session["snippetId"],
                language=session["language"],
                score=score_data["total_score"],
                difficulty=session["difficulty"],
                similarity=score_data["accuracy"],
                time_taken=request.time_taken
            )
        
        return ScoreResponse(
            session_id=request.session_id,
            total_score=score_data["total_score"],
            accuracy=score_data["accuracy"],
            time_bonus=score_data["time_bonus"],
            mistakes=score_data["mistakes"],
            time_taken=score_data["time_taken"],
            detailed_results=detailed_results,
            leaderboard_eligible=leaderboard_eligible
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to submit practice attempt: {str(e)}"
        )


async def _add_to_leaderboard(
    user_id: str,
    snippet_id: str,
    language: str,
    score: float,
    difficulty: int,
    similarity: float,
    time_taken: float
):
    """Add entry to leaderboard"""
    try:
        leaderboard_collection = await get_leaderboard_collection()
        users_collection = await get_users_collection()
        
        # Get user info
        user = await users_collection.find_one({"_id": user_id}, {"name": 1})
        user_name = user["name"] if user else "Unknown"
        
        # Create leaderboard entry
        entry_id = generate_id()
        entry = {
            "_id": entry_id,
            "leaderboard_type": language,
            "userId": user_id,
            "userName": user_name,
            "snippetId": snippet_id,
            "score": int(score),
            "rank": None,  # Will be calculated later
            "similarity": similarity,
            "difficulty": difficulty,
            "timeSpent": time_taken,
            "dateOfSubmission": current_timestamp()
        }
        
        await leaderboard_collection.insert_one(entry)
        
    except Exception as e:
        # Don't fail the practice submission if leaderboard update fails
        print(f"Failed to add to leaderboard: {str(e)}")


@app.get("/session/{session_id}")
async def get_practice_session(
    session_id: str,
    user_data: Dict[str, Any] = Depends(verify_token)
):
    """
    Get practice session details
    """
    try:
        practice_sessions_collection = await get_practice_sessions_collection()
        
        # Validate session ID
        try:
            ObjectId(session_id)
        except:
            raise HTTPException(status_code=400, detail="Invalid session ID")
        
        session = await practice_sessions_collection.find_one({"_id": session_id})
        
        if not session:
            raise HTTPException(status_code=404, detail="Practice session not found")
        
        # Verify ownership
        if session["userId"] != user_data["user_id"]:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Format response
        response_data = {
            "session_id": session_id,
            "snippet_id": session["snippetId"],
            "language": session["language"],
            "difficulty": session["difficulty"],
            "masked_code": session["maskedCode"],
            "completed": session["completed"],
            "created_at": session["createdAt"].isoformat(),
            "answer_count": len(session["correctAnswers"])
        }
        
        # Add completion data if available
        if session["completed"]:
            response_data.update({
                "score": session.get("score"),
                "time_spent": session.get("timeSpent"),
                "mistakes": session.get("mistakes"),
                "completed_at": session["completedAt"].isoformat() if session.get("completedAt") else None
            })
        
        return create_response(response_data)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get practice session: {str(e)}"
        )


@app.get("/history")
async def get_practice_history(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    language: Optional[str] = Query(None),
    completed_only: bool = Query(True),
    user_data: Dict[str, Any] = Depends(verify_token)
):
    """
    Get user's practice history
    """
    try:
        practice_sessions_collection = await get_practice_sessions_collection()
        snippets_collection = await get_snippets_collection()
        
        user_id = user_data["user_id"]
        
        # Build query
        query = {"userId": user_id}
        
        if completed_only:
            query["completed"] = True
        
        if language:
            query["language"] = language
        
        # Get sessions with pagination
        cursor = practice_sessions_collection.find(query).sort("createdAt", -1)
        total_count = await practice_sessions_collection.count_documents(query)
        
        # Calculate pagination
        skip = (page - 1) * per_page
        sessions = await cursor.skip(skip).limit(per_page).to_list(per_page)
        
        # Get snippet info for sessions
        snippet_ids = [session["snippetId"] for session in sessions]
        snippets = await snippets_collection.find(
            {"_id": {"$in": snippet_ids}},
            {"title": 1, "type": 1}
        ).to_list(None)
        snippet_info = {str(snippet["_id"]): snippet for snippet in snippets}
        
        # Format response
        formatted_sessions = []
        for session in sessions:
            snippet = snippet_info.get(session["snippetId"], {})
            
            session_data = {
                "session_id": str(session["_id"]),
                "snippet_id": session["snippetId"],
                "snippet_title": snippet.get("title", "Unknown"),
                "snippet_type": snippet.get("type", "unknown"),
                "language": session["language"],
                "difficulty": session["difficulty"],
                "completed": session["completed"],
                "created_at": session["createdAt"].isoformat()
            }
            
            if session["completed"]:
                score = session.get("score", {})
                session_data.update({
                    "total_score": score.get("total_score", 0),
                    "accuracy": score.get("accuracy", 0),
                    "time_taken": score.get("time_taken", 0),
                    "mistakes": score.get("mistakes", 0),
                    "completed_at": session["completedAt"].isoformat() if session.get("completedAt") else None
                })
            
            formatted_sessions.append(session_data)
        
        # Paginate results
        total_pages = (total_count + per_page - 1) // per_page
        
        return create_response({
            "sessions": formatted_sessions,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total_count": total_count,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_prev": page > 1
            }
        })
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get practice history: {str(e)}"
        )


@app.get("/stats")
async def get_practice_stats(
    user_data: Dict[str, Any] = Depends(verify_token)
):
    """
    Get user's practice statistics
    """
    try:
        practice_sessions_collection = await get_practice_sessions_collection()
        user_id = user_data["user_id"]
        
        # Aggregate practice statistics
        pipeline = [
            {"$match": {"userId": user_id, "completed": True}},
            {
                "$group": {
                    "_id": None,
                    "total_sessions": {"$sum": 1},
                    "avg_score": {"$avg": "$score.total_score"},
                    "avg_accuracy": {"$avg": "$score.accuracy"},
                    "total_time": {"$sum": "$timeSpent"},
                    "total_mistakes": {"$sum": "$score.mistakes"}
                }
            }
        ]
        
        result = await practice_sessions_collection.aggregate(pipeline).to_list(1)
        stats = result[0] if result else {}
        
        # Language breakdown
        language_pipeline = [
            {"$match": {"userId": user_id, "completed": True}},
            {
                "$group": {
                    "_id": "$language",
                    "sessions": {"$sum": 1},
                    "avg_score": {"$avg": "$score.total_score"},
                    "avg_accuracy": {"$avg": "$score.accuracy"}
                }
            }
        ]
        
        language_stats = await practice_sessions_collection.aggregate(language_pipeline).to_list(None)
        
        # Format response
        formatted_stats = {
            "total_sessions": stats.get("total_sessions", 0),
            "average_score": round(stats.get("avg_score", 0), 2),
            "average_accuracy": round(stats.get("avg_accuracy", 0), 3),
            "total_practice_time": round(stats.get("total_time", 0), 1),
            "total_mistakes": stats.get("total_mistakes", 0),
            "languages": {
                lang["_id"]: {
                    "sessions": lang["sessions"],
                    "avg_score": round(lang["avg_score"], 2),
                    "avg_accuracy": round(lang["avg_accuracy"], 3)
                }
                for lang in language_stats
            }
        }
        
        return create_response(formatted_stats)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get practice stats: {str(e)}"
        )


@functions_framework.http
def main(request):
    """Cloud Function entry point"""
    return app(request.environ, lambda status, headers: None)