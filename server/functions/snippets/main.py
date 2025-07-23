"""
Snippets Management Cloud Function for SyntaxMem
Handles official snippets, personal snippets, submissions, and code masking
"""
import functions_framework
from fastapi import FastAPI, HTTPException, status, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from bson import ObjectId
import sys
import os
from a2wsgi import ASGIMiddleware


# Add shared modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from shared.database import (
    get_snippets_collection, 
    get_users_collection,
    get_practice_sessions_collection
)
from shared.auth_middleware import verify_token, verify_admin, optional_auth
from shared.masking import mask_code
from shared.utils import (
    generate_id, current_timestamp, create_response, create_error_response,
    sanitize_code, sanitize_text, validate_language, normalize_language,
    paginate_results, clean_user_input
)

app = FastAPI(title="SyntaxMem Snippets Service")

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
class CreateSnippetRequest(BaseModel):
    """Create new snippet request"""
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=10, max_length=10000)
    language: str = Field(..., pattern="^(python|javascript)$")
    difficulty: int = Field(..., ge=1, le=10)
    is_public: bool = False


class SubmitSnippetRequest(BaseModel):
    """Submit snippet for review request"""
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=10, max_length=10000)
    language: str = Field(..., pattern="^(python|javascript)$")
    difficulty: int = Field(..., ge=1, le=10)
    description: str = Field("", max_length=500)


class ReviewSnippetRequest(BaseModel):
    """Admin review snippet request"""
    action: str = Field(..., pattern="^(approve|reject)$")
    review_notes: str = Field("", max_length=500)


class MaskCodeRequest(BaseModel):
    """Mask code for practice request"""
    snippet_id: str
    difficulty: Optional[int] = Field(None, ge=1, le=10)


class SnippetResponse(BaseModel):
    """Snippet response model"""
    id: str
    title: str
    content: str
    language: str
    difficulty: int
    type: str
    status: str
    author_name: str
    solve_count: int
    avg_score: float
    created_at: str


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return create_response({"status": "healthy", "service": "snippets"})


@app.get("/official")
async def get_official_snippets(
    language: Optional[str] = Query(None),
    difficulty: Optional[int] = Query(None, ge=1, le=10),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    user_data: Optional[Dict[str, Any]] = Depends(optional_auth)
):
    """
    Get official snippets (curated, count towards leaderboard)
    """
    try:
        snippets_collection = await get_snippets_collection()
        
        # Build query
        query = {
            "type": "official",
            "status": "active"
        }
        
        if language:
            if not validate_language(language):
                raise HTTPException(status_code=400, detail="Invalid language")
            query["language"] = normalize_language(language)
        
        if difficulty:
            query["difficulty"] = difficulty
        
        # Get snippets with pagination
        cursor = snippets_collection.find(query).sort("createdAt", -1)
        total_count = await snippets_collection.count_documents(query)
        
        # Calculate pagination
        skip = (page - 1) * per_page
        snippets = await cursor.skip(skip).limit(per_page).to_list(per_page)
        
        # Get author names
        user_ids = [snippet.get("author") for snippet in snippets if snippet.get("author")]
        users_collection = await get_users_collection()
        users = await users_collection.find(
            {"_id": {"$in": user_ids}}, 
            {"name": 1}
        ).to_list(None)
        user_names = {str(user["_id"]): user["name"] for user in users}
        
        # Format response
        formatted_snippets = []
        for snippet in snippets:
            formatted_snippets.append({
                "id": str(snippet["_id"]),
                "title": snippet["title"],
                "language": snippet["language"],
                "difficulty": snippet["difficulty"],
                "type": snippet["type"],
                "author_name": user_names.get(snippet.get("author", ""), "Unknown"),
                "solve_count": snippet.get("solveCount", 0),
                "avg_score": snippet.get("avgScore", 0.0),
                "created_at": snippet["createdAt"].isoformat() if snippet.get("createdAt") else ""
            })
        
        # Paginate results
        total_pages = (total_count + per_page - 1) // per_page
        
        return create_response({
            "snippets": formatted_snippets,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total_count": total_count,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_prev": page > 1
            }
        })
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get official snippets: {str(e)}"
        )


@app.get("/personal")
async def get_personal_snippets(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    user_data: Dict[str, Any] = Depends(verify_token)
):
    """
    Get user's personal snippets (private practice only)
    """
    try:
        snippets_collection = await get_snippets_collection()
        user_id = user_data["user_id"]
        
        # Query user's personal snippets
        query = {
            "type": "personal",
            "author": user_id
        }
        
        cursor = snippets_collection.find(query).sort("createdAt", -1)
        total_count = await snippets_collection.count_documents(query)
        
        # Calculate pagination
        skip = (page - 1) * per_page
        snippets = await cursor.skip(skip).limit(per_page).to_list(per_page)
        
        # Format response
        formatted_snippets = []
        for snippet in snippets:
            formatted_snippets.append({
                "id": str(snippet["_id"]),
                "title": snippet["title"],
                "content": snippet["content"],  # Include content for personal snippets
                "language": snippet["language"],
                "difficulty": snippet["difficulty"],
                "type": snippet["type"],
                "created_at": snippet["createdAt"].isoformat() if snippet.get("createdAt") else ""
            })
        
        # Paginate results
        total_pages = (total_count + per_page - 1) // per_page
        
        return create_response({
            "snippets": formatted_snippets,
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
            detail=f"Failed to get personal snippets: {str(e)}"
        )


@app.get("/{snippet_id}")
async def get_snippet_by_id(
    snippet_id: str,
    user_data: Optional[Dict[str, Any]] = Depends(optional_auth)
):
    """
    Get specific snippet by ID
    """
    try:
        snippets_collection = await get_snippets_collection()
        
        # Validate ObjectId
        try:
            ObjectId(snippet_id)
        except:
            raise HTTPException(status_code=400, detail="Invalid snippet ID")
        
        snippet = await snippets_collection.find_one({"_id": snippet_id})
        
        if not snippet:
            raise HTTPException(status_code=404, detail="Snippet not found")
        
        # Check permissions
        if snippet["type"] == "personal":
            if not user_data or user_data["user_id"] != snippet["author"]:
                raise HTTPException(status_code=403, detail="Access denied")
        elif snippet["type"] == "official" and snippet["status"] != "active":
            if not user_data or user_data["user"].get("role") != "admin":
                raise HTTPException(status_code=403, detail="Access denied")
        
        # Get author name
        users_collection = await get_users_collection()
        author = await users_collection.find_one({"_id": snippet["author"]}, {"name": 1})
        author_name = author["name"] if author else "Unknown"
        
        return create_response({
            "id": str(snippet["_id"]),
            "title": snippet["title"],
            "content": snippet["content"],
            "language": snippet["language"],
            "difficulty": snippet["difficulty"],
            "type": snippet["type"],
            "status": snippet.get("status", "active"),
            "author_name": author_name,
            "solve_count": snippet.get("solveCount", 0),
            "avg_score": snippet.get("avgScore", 0.0),
            "created_at": snippet["createdAt"].isoformat() if snippet.get("createdAt") else ""
        })
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get snippet: {str(e)}"
        )


@app.post("/create")
async def create_personal_snippet(
    snippet_data: CreateSnippetRequest,
    user_data: Dict[str, Any] = Depends(verify_token)
):
    """
    Create new personal snippet (private practice only)
    """
    try:
        snippets_collection = await get_snippets_collection()
        user_id = user_data["user_id"]
        
        # Validate and clean input
        cleaned_data = clean_user_input(snippet_data.dict())
        
        if not validate_language(cleaned_data["language"]):
            raise HTTPException(status_code=400, detail="Invalid language")
        
        # Create snippet
        snippet_id = generate_id()
        new_snippet = {
            "_id": snippet_id,
            "title": sanitize_text(cleaned_data["title"], 100),
            "content": sanitize_code(cleaned_data["content"]),
            "language": normalize_language(cleaned_data["language"]),
            "difficulty": cleaned_data["difficulty"],
            "type": "personal",
            "status": "active",
            "author": user_id,
            "isPublic": cleaned_data.get("is_public", False),
            "solveCount": 0,
            "avgScore": 0.0,
            "createdAt": current_timestamp()
        }
        
        await snippets_collection.insert_one(new_snippet)
        
        return create_response(
            data={"snippet_id": snippet_id},
            message="Personal snippet created successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create snippet: {str(e)}"
        )


@app.post("/submit")
async def submit_snippet_for_review(
    submission_data: SubmitSnippetRequest,
    user_data: Dict[str, Any] = Depends(verify_token)
):
    """
    Submit snippet for admin review (to become official)
    """
    try:
        snippets_collection = await get_snippets_collection()
        user_id = user_data["user_id"]
        
        # Validate and clean input
        cleaned_data = clean_user_input(submission_data.dict())
        
        if not validate_language(cleaned_data["language"]):
            raise HTTPException(status_code=400, detail="Invalid language")
        
        # Create submission
        snippet_id = generate_id()
        submission = {
            "_id": snippet_id,
            "title": sanitize_text(cleaned_data["title"], 100),
            "content": sanitize_code(cleaned_data["content"]),
            "language": normalize_language(cleaned_data["language"]),
            "difficulty": cleaned_data["difficulty"],
            "type": "official",
            "status": "pending",
            "author": user_id,
            "originalAuthor": user_id,
            "description": sanitize_text(cleaned_data.get("description", ""), 500),
            "submittedAt": current_timestamp(),
            "reviewedAt": None,
            "reviewNotes": "",
            "isPublic": True,
            "solveCount": 0,
            "avgScore": 0.0,
            "createdAt": current_timestamp()
        }
        
        await snippets_collection.insert_one(submission)
        
        return create_response(
            data={"submission_id": snippet_id},
            message="Snippet submitted for review successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to submit snippet: {str(e)}"
        )


@app.get("/submissions")
async def get_user_submissions(
    user_data: Dict[str, Any] = Depends(verify_token)
):
    """
    Get user's snippet submissions and their status
    """
    try:
        snippets_collection = await get_snippets_collection()
        user_id = user_data["user_id"]
        
        # Get user's submissions
        submissions = await snippets_collection.find({
            "originalAuthor": user_id,
            "type": "official"
        }).sort("submittedAt", -1).to_list(None)
        
        formatted_submissions = []
        for submission in submissions:
            formatted_submissions.append({
                "id": str(submission["_id"]),
                "title": submission["title"],
                "language": submission["language"],
                "difficulty": submission["difficulty"],
                "status": submission["status"],
                "submitted_at": submission["submittedAt"].isoformat() if submission.get("submittedAt") else "",
                "reviewed_at": submission["reviewedAt"].isoformat() if submission.get("reviewedAt") else None,
                "review_notes": submission.get("reviewNotes", "")
            })
        
        return create_response({"submissions": formatted_submissions})
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get submissions: {str(e)}"
        )


@app.post("/{snippet_id}/mask")
async def get_masked_snippet(
    snippet_id: str,
    mask_request: MaskCodeRequest,
    user_data: Optional[Dict[str, Any]] = Depends(optional_auth)
):
    """
    Get masked version of snippet for practice
    """
    try:
        snippets_collection = await get_snippets_collection()
        
        # Validate ObjectId
        try:
            ObjectId(snippet_id)
        except:
            raise HTTPException(status_code=400, detail="Invalid snippet ID")
        
        snippet = await snippets_collection.find_one({"_id": snippet_id})
        
        if not snippet:
            raise HTTPException(status_code=404, detail="Snippet not found")
        
        # Check permissions
        if snippet["type"] == "personal":
            if not user_data or user_data["user_id"] != snippet["author"]:
                raise HTTPException(status_code=403, detail="Access denied")
        elif snippet["type"] == "official" and snippet["status"] != "active":
            raise HTTPException(status_code=403, detail="Snippet not available for practice")
        
        # Use custom difficulty or snippet's default
        difficulty = mask_request.difficulty or snippet["difficulty"]
        
        # Mask the code
        masked_code, answers = mask_code(
            snippet["content"],
            snippet["language"],
            difficulty
        )
        
        return create_response({
            "snippet_id": snippet_id,
            "title": snippet["title"],
            "language": snippet["language"],
            "difficulty": difficulty,
            "masked_code": masked_code,
            "answer_count": len(answers),
            "type": snippet["type"]
        })
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to mask snippet: {str(e)}"
        )


# Admin endpoints
@app.get("/admin/pending")
async def get_pending_submissions(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    admin_data: Dict[str, Any] = Depends(verify_admin)
):
    """
    Get pending snippet submissions for review (admin only)
    """
    try:
        snippets_collection = await get_snippets_collection()
        
        # Get pending submissions
        query = {"status": "pending", "type": "official"}
        cursor = snippets_collection.find(query).sort("submittedAt", 1)
        total_count = await snippets_collection.count_documents(query)
        
        # Calculate pagination
        skip = (page - 1) * per_page
        submissions = await cursor.skip(skip).limit(per_page).to_list(per_page)
        
        # Get author names
        user_ids = [sub.get("originalAuthor") for sub in submissions if sub.get("originalAuthor")]
        users_collection = await get_users_collection()
        users = await users_collection.find(
            {"_id": {"$in": user_ids}}, 
            {"name": 1, "email": 1}
        ).to_list(None)
        user_info = {str(user["_id"]): user for user in users}
        
        # Format response
        formatted_submissions = []
        for submission in submissions:
            author_info = user_info.get(submission.get("originalAuthor", ""), {})
            formatted_submissions.append({
                "id": str(submission["_id"]),
                "title": submission["title"],
                "content": submission["content"],
                "language": submission["language"],
                "difficulty": submission["difficulty"],
                "description": submission.get("description", ""),
                "author_name": author_info.get("name", "Unknown"),
                "author_email": author_info.get("email", ""),
                "submitted_at": submission["submittedAt"].isoformat() if submission.get("submittedAt") else ""
            })
        
        # Paginate results
        total_pages = (total_count + per_page - 1) // per_page
        
        return create_response({
            "submissions": formatted_submissions,
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
            detail=f"Failed to get pending submissions: {str(e)}"
        )


@app.put("/admin/{snippet_id}/review")
async def review_snippet_submission(
    snippet_id: str,
    review_data: ReviewSnippetRequest,
    admin_data: Dict[str, Any] = Depends(verify_admin)
):
    """
    Approve or reject snippet submission (admin only)
    """
    try:
        snippets_collection = await get_snippets_collection()
        
        # Validate ObjectId
        try:
            ObjectId(snippet_id)
        except:
            raise HTTPException(status_code=400, detail="Invalid snippet ID")
        
        snippet = await snippets_collection.find_one({"_id": snippet_id})
        
        if not snippet:
            raise HTTPException(status_code=404, detail="Snippet not found")
        
        if snippet["status"] != "pending":
            raise HTTPException(status_code=400, detail="Snippet is not pending review")
        
        # Update snippet status
        new_status = "active" if review_data.action == "approve" else "rejected"
        
        await snippets_collection.update_one(
            {"_id": snippet_id},
            {
                "$set": {
                    "status": new_status,
                    "reviewedAt": current_timestamp(),
                    "reviewNotes": sanitize_text(review_data.review_notes, 500),
                    "author": admin_data["user_id"]  # Admin becomes the author for approved snippets
                }
            }
        )
        
        action_text = "approved" if review_data.action == "approve" else "rejected"
        return create_response(
            message=f"Snippet {action_text} successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to review snippet: {str(e)}"
        )


@functions_framework.http  
def main(request):
    """Cloud Function entry point"""
    import asyncio
    import json
    from werkzeug.wrappers import Response
    
    # Set up event loop
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        response = Response('')
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'  
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response
    
    try:
        # Manually route the request to FastAPI endpoints
        path = request.path.strip('/')
        method = request.method
        
        # Simple routing
        if path == 'health' and method == 'GET':
            result = loop.run_until_complete(health_check())
        elif path == 'official' and method == 'GET':
            # Get query parameters
            language = request.args.get('language')
            difficulty = request.args.get('difficulty', type=int)
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 20, type=int)
            
            result = loop.run_until_complete(get_official_snippets(
                language=language,
                difficulty=difficulty, 
                page=page,
                per_page=per_page,
                user_data=None  # No auth for official snippets
            ))
        elif path == 'personal' and method == 'GET':
            # This requires authentication - return 401 for now
            result = {"status": "error", "message": "Authentication required", "data": None}
        else:
            result = {"status": "error", "message": "Endpoint not found", "data": None}
        
        # Create response
        response_data = json.dumps(result)
        response = Response(response_data, content_type='application/json')
        
        # Add CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        
        return response
        
    except Exception as e:
        # Error response with CORS headers
        error_response = {
            "status": "error", 
            "message": f"Internal server error: {str(e)}", 
            "data": None
        }
        response = Response(
            json.dumps(error_response), 
            status=500,
            content_type='application/json'
        )
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        
        return response