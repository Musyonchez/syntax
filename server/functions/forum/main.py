"""
Forum Cloud Function for SyntaxMem
Handles developer-user communication with posts, comments, and voting
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
    get_forum_posts_collection,
    get_forum_comments_collection,
    get_user_votes_collection,
    get_users_collection
)
from shared.auth_middleware import verify_token, verify_admin, optional_auth
from shared.utils import (
    generate_id, current_timestamp, create_response, create_error_response,
    sanitize_text, clean_user_input, paginate_results
)

app = FastAPI(title="SyntaxMem Forum Service")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://syntaxmem.dev", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response models
class CreatePostRequest(BaseModel):
    """Create forum post request (dev only)"""
    title: str = Field(..., min_length=5, max_length=200)
    content: str = Field(..., min_length=10, max_length=5000)
    type: str = Field(..., regex="^(announcement|question|update)$")
    is_pinned: bool = False


class CreateCommentRequest(BaseModel):
    """Create comment request"""
    post_id: str
    content: str = Field(..., min_length=1, max_length=2000)
    parent_id: Optional[str] = None  # For nested replies


class VoteRequest(BaseModel):
    """Vote request"""
    target_id: str  # Post or comment ID
    target_type: str = Field(..., regex="^(post|comment)$")
    vote_type: str = Field(..., regex="^(up|down)$")


class ForumPostResponse(BaseModel):
    """Forum post response"""
    id: str
    title: str
    content: str
    type: str
    author_name: str
    author_avatar: str
    is_pinned: bool
    votes: Dict[str, int]
    comment_count: int
    created_at: str
    updated_at: str
    user_vote: Optional[str] = None


class CommentResponse(BaseModel):
    """Comment response"""
    id: str
    post_id: str
    parent_id: Optional[str]
    content: str
    author_name: str
    author_avatar: str
    votes: Dict[str, int]
    score: int
    depth: int
    created_at: str
    updated_at: str
    user_vote: Optional[str] = None
    replies: List['CommentResponse'] = []


# Add forward reference
CommentResponse.model_rebuild()


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return create_response({"status": "healthy", "service": "forum"})


@app.get("/posts")
async def get_forum_posts(
    type_filter: Optional[str] = Query(None, regex="^(announcement|question|update)$"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=50),
    user_data: Optional[Dict[str, Any]] = Depends(optional_auth)
):
    """
    Get forum posts with optional filtering and pagination
    """
    try:
        posts_collection = await get_forum_posts_collection()
        users_collection = await get_users_collection()
        votes_collection = await get_user_votes_collection()
        
        # Build query
        query = {}
        if type_filter:
            query["type"] = type_filter
        
        # Get posts with pagination, pinned posts first
        cursor = posts_collection.find(query).sort([("isPinned", -1), ("createdAt", -1)])
        total_count = await posts_collection.count_documents(query)
        
        # Calculate pagination
        skip = (page - 1) * per_page
        posts = await cursor.skip(skip).limit(per_page).to_list(per_page)
        
        # Get author information
        author_ids = [post.get("author") for post in posts if post.get("author")]
        authors = await users_collection.find(
            {"_id": {"$in": author_ids}},
            {"name": 1, "avatar": 1}
        ).to_list(None)
        author_info = {str(author["_id"]): author for author in authors}
        
        # Get user votes if authenticated
        user_votes = {}
        if user_data:
            user_id = user_data["user_id"]
            post_ids = [str(post["_id"]) for post in posts]
            votes = await votes_collection.find({
                "userId": user_id,
                "targetId": {"$in": post_ids},
                "targetType": "post"
            }).to_list(None)
            user_votes = {vote["targetId"]: vote["voteType"] for vote in votes}
        
        # Format posts
        formatted_posts = []
        for post in posts:
            post_id = str(post["_id"])
            author = author_info.get(post.get("author", ""), {})
            
            formatted_post = ForumPostResponse(
                id=post_id,
                title=post["title"],
                content=post["content"],
                type=post["type"],
                author_name=author.get("name", "Developer"),
                author_avatar=author.get("avatar", ""),
                is_pinned=post.get("isPinned", False),
                votes=post.get("votes", {"up": 0, "down": 0}),
                comment_count=post.get("commentCount", 0),
                created_at=post["createdAt"].isoformat(),
                updated_at=post.get("updatedAt", post["createdAt"]).isoformat(),
                user_vote=user_votes.get(post_id)
            )
            
            formatted_posts.append(formatted_post)
        
        # Calculate pagination info
        total_pages = (total_count + per_page - 1) // per_page
        
        return create_response({
            "posts": [post.dict() for post in formatted_posts],
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
            detail=f"Failed to get forum posts: {str(e)}"
        )


@app.post("/posts")
async def create_forum_post(
    post_data: CreatePostRequest,
    admin_data: Dict[str, Any] = Depends(verify_admin)
):
    """
    Create new forum post (admin/dev only)
    """
    try:
        posts_collection = await get_forum_posts_collection()
        
        # Clean and validate input
        cleaned_data = clean_user_input(post_data.dict())
        
        # Create post
        post_id = generate_id()
        new_post = {
            "_id": post_id,
            "title": sanitize_text(cleaned_data["title"], 200),
            "content": sanitize_text(cleaned_data["content"], 5000),
            "type": cleaned_data["type"],
            "author": admin_data["user_id"],
            "isPinned": cleaned_data.get("is_pinned", False),
            "votes": {"up": 0, "down": 0},
            "commentCount": 0,
            "createdAt": current_timestamp(),
            "updatedAt": current_timestamp()
        }
        
        await posts_collection.insert_one(new_post)
        
        return create_response(
            data={"post_id": post_id},
            message="Forum post created successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create forum post: {str(e)}"
        )


@app.get("/posts/{post_id}")
async def get_forum_post(
    post_id: str,
    user_data: Optional[Dict[str, Any]] = Depends(optional_auth)
):
    """
    Get specific forum post with details
    """
    try:
        posts_collection = await get_forum_posts_collection()
        users_collection = await get_users_collection()
        votes_collection = await get_user_votes_collection()
        
        # Validate post ID
        try:
            ObjectId(post_id)
        except:
            raise HTTPException(status_code=400, detail="Invalid post ID")
        
        # Get post
        post = await posts_collection.find_one({"_id": post_id})
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        
        # Get author info
        author = await users_collection.find_one(
            {"_id": post.get("author")},
            {"name": 1, "avatar": 1}
        )
        
        # Get user vote if authenticated
        user_vote = None
        if user_data:
            vote = await votes_collection.find_one({
                "userId": user_data["user_id"],
                "targetId": post_id,
                "targetType": "post"
            })
            user_vote = vote["voteType"] if vote else None
        
        # Format response
        formatted_post = ForumPostResponse(
            id=post_id,
            title=post["title"],
            content=post["content"],
            type=post["type"],
            author_name=author.get("name", "Developer") if author else "Developer",
            author_avatar=author.get("avatar", "") if author else "",
            is_pinned=post.get("isPinned", False),
            votes=post.get("votes", {"up": 0, "down": 0}),
            comment_count=post.get("commentCount", 0),
            created_at=post["createdAt"].isoformat(),
            updated_at=post.get("updatedAt", post["createdAt"]).isoformat(),
            user_vote=user_vote
        )
        
        return create_response(formatted_post.dict())
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get forum post: {str(e)}"
        )


@app.get("/posts/{post_id}/comments")
async def get_post_comments(
    post_id: str,
    sort_by: str = Query("score", regex="^(score|date)$"),
    user_data: Optional[Dict[str, Any]] = Depends(optional_auth)
):
    """
    Get comments for a forum post with threaded replies
    """
    try:
        comments_collection = await get_forum_comments_collection()
        users_collection = await get_users_collection()
        votes_collection = await get_user_votes_collection()
        
        # Validate post ID
        try:
            ObjectId(post_id)
        except:
            raise HTTPException(status_code=400, detail="Invalid post ID")
        
        # Get all comments for the post
        sort_field = "votes.score" if sort_by == "score" else "createdAt"
        sort_order = -1 if sort_by == "score" else 1
        
        comments = await comments_collection.find(
            {"postId": post_id}
        ).sort(sort_field, sort_order).to_list(None)
        
        if not comments:
            return create_response({"comments": []})
        
        # Get author information
        author_ids = [comment.get("author") for comment in comments if comment.get("author")]
        authors = await users_collection.find(
            {"_id": {"$in": author_ids}},
            {"name": 1, "avatar": 1}
        ).to_list(None)
        author_info = {str(author["_id"]): author for author in authors}
        
        # Get user votes if authenticated
        user_votes = {}
        if user_data:
            user_id = user_data["user_id"]
            comment_ids = [str(comment["_id"]) for comment in comments]
            votes = await votes_collection.find({
                "userId": user_id,
                "targetId": {"$in": comment_ids},
                "targetType": "comment"
            }).to_list(None)
            user_votes = {vote["targetId"]: vote["voteType"] for vote in votes}
        
        # Build threaded comment structure
        comment_map = {}
        root_comments = []
        
        # First pass: create comment objects
        for comment in comments:
            comment_id = str(comment["_id"])
            author = author_info.get(comment.get("author", ""), {})
            
            comment_obj = CommentResponse(
                id=comment_id,
                post_id=post_id,
                parent_id=comment.get("parentId"),
                content=comment["content"],
                author_name=author.get("name", "User"),
                author_avatar=author.get("avatar", ""),
                votes=comment.get("votes", {"up": 0, "down": 0}),
                score=comment.get("votes", {}).get("score", 0),
                depth=comment.get("depth", 0),
                created_at=comment["createdAt"].isoformat(),
                updated_at=comment.get("updatedAt", comment["createdAt"]).isoformat(),
                user_vote=user_votes.get(comment_id),
                replies=[]
            )
            
            comment_map[comment_id] = comment_obj
            
            # If no parent, it's a root comment
            if not comment.get("parentId"):
                root_comments.append(comment_obj)
        
        # Second pass: build reply chains
        for comment in comments:
            comment_id = str(comment["_id"])
            parent_id = comment.get("parentId")
            
            if parent_id and parent_id in comment_map:
                comment_map[parent_id].replies.append(comment_map[comment_id])
        
        # Sort root comments by score/date
        if sort_by == "score":
            root_comments.sort(key=lambda c: c.score, reverse=True)
        else:
            root_comments.sort(key=lambda c: c.created_at)
        
        # Sort replies recursively
        def sort_replies(comment_list):
            for comment in comment_list:
                if comment.replies:
                    if sort_by == "score":
                        comment.replies.sort(key=lambda c: c.score, reverse=True)
                    else:
                        comment.replies.sort(key=lambda c: c.created_at)
                    sort_replies(comment.replies)
        
        sort_replies(root_comments)
        
        return create_response({
            "comments": [comment.dict() for comment in root_comments],
            "total_count": len(comments),
            "sort_by": sort_by
        })
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get post comments: {str(e)}"
        )


@app.post("/comments")
async def create_comment(
    comment_data: CreateCommentRequest,
    user_data: Dict[str, Any] = Depends(verify_token)
):
    """
    Create new comment or reply
    """
    try:
        comments_collection = await get_forum_comments_collection()
        posts_collection = await get_forum_posts_collection()
        
        # Validate post exists
        try:
            ObjectId(comment_data.post_id)
        except:
            raise HTTPException(status_code=400, detail="Invalid post ID")
        
        post = await posts_collection.find_one({"_id": comment_data.post_id})
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        
        # Validate parent comment if replying
        depth = 0
        if comment_data.parent_id:
            try:
                ObjectId(comment_data.parent_id)
            except:
                raise HTTPException(status_code=400, detail="Invalid parent comment ID")
            
            parent_comment = await comments_collection.find_one({"_id": comment_data.parent_id})
            if not parent_comment:
                raise HTTPException(status_code=404, detail="Parent comment not found")
            
            # Limit nesting depth to prevent deep threading
            depth = parent_comment.get("depth", 0) + 1
            if depth > 5:  # Max 5 levels deep
                raise HTTPException(status_code=400, detail="Maximum reply depth exceeded")
        
        # Clean input
        cleaned_data = clean_user_input(comment_data.dict())
        
        # Create comment
        comment_id = generate_id()
        new_comment = {
            "_id": comment_id,
            "postId": comment_data.post_id,
            "parentId": comment_data.parent_id,
            "content": sanitize_text(cleaned_data["content"], 2000),
            "author": user_data["user_id"],
            "votes": {"up": 0, "down": 0, "score": 0},
            "depth": depth,
            "createdAt": current_timestamp(),
            "updatedAt": current_timestamp()
        }
        
        await comments_collection.insert_one(new_comment)
        
        # Update post comment count
        await posts_collection.update_one(
            {"_id": comment_data.post_id},
            {"$inc": {"commentCount": 1}}
        )
        
        return create_response(
            data={"comment_id": comment_id},
            message="Comment created successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create comment: {str(e)}"
        )


@app.post("/vote")
async def vote_on_content(
    vote_data: VoteRequest,
    user_data: Dict[str, Any] = Depends(verify_token)
):
    """
    Vote on post or comment (upvote/downvote)
    """
    try:
        votes_collection = await get_user_votes_collection()
        posts_collection = await get_forum_posts_collection()
        comments_collection = await get_forum_comments_collection()
        
        user_id = user_data["user_id"]
        target_id = vote_data.target_id
        target_type = vote_data.target_type
        vote_type = vote_data.vote_type
        
        # Validate target exists
        try:
            ObjectId(target_id)
        except:
            raise HTTPException(status_code=400, detail="Invalid target ID")
        
        # Get target collection
        target_collection = posts_collection if target_type == "post" else comments_collection
        target = await target_collection.find_one({"_id": target_id})
        
        if not target:
            raise HTTPException(status_code=404, detail=f"{target_type.title()} not found")
        
        # Check if user already voted
        existing_vote = await votes_collection.find_one({
            "userId": user_id,
            "targetId": target_id,
            "targetType": target_type
        })
        
        vote_change = 0
        current_votes = target.get("votes", {"up": 0, "down": 0})
        
        if existing_vote:
            old_vote_type = existing_vote["voteType"]
            
            if old_vote_type == vote_type:
                # Remove vote (toggle)
                await votes_collection.delete_one({"_id": existing_vote["_id"]})
                vote_change = -1 if vote_type == "up" else 1
            else:
                # Change vote
                await votes_collection.update_one(
                    {"_id": existing_vote["_id"]},
                    {"$set": {"voteType": vote_type, "createdAt": current_timestamp()}}
                )
                vote_change = 2 if vote_type == "up" else -2
        else:
            # New vote
            vote_id = generate_id()
            new_vote = {
                "_id": vote_id,
                "userId": user_id,
                "targetId": target_id,
                "targetType": target_type,
                "voteType": vote_type,
                "createdAt": current_timestamp()
            }
            
            await votes_collection.insert_one(new_vote)
            vote_change = 1 if vote_type == "up" else -1
        
        # Update vote counts
        if vote_type == "up":
            new_up = max(0, current_votes.get("up", 0) + vote_change)
            new_down = current_votes.get("down", 0)
        else:
            new_up = current_votes.get("up", 0)
            new_down = max(0, current_votes.get("down", 0) + abs(vote_change))
        
        # Calculate score (up - down)
        score = new_up - new_down
        
        # Update target document
        await target_collection.update_one(
            {"_id": target_id},
            {
                "$set": {
                    "votes.up": new_up,
                    "votes.down": new_down,
                    "votes.score": score,
                    "updatedAt": current_timestamp()
                }
            }
        )
        
        return create_response({
            "target_id": target_id,
            "target_type": target_type,
            "votes": {
                "up": new_up,
                "down": new_down,
                "score": score
            },
            "user_vote": vote_type if not (existing_vote and existing_vote["voteType"] == vote_type) else None
        })
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process vote: {str(e)}"
        )


@app.put("/posts/{post_id}")
async def update_forum_post(
    post_id: str,
    update_data: Dict[str, Any],
    admin_data: Dict[str, Any] = Depends(verify_admin)
):
    """
    Update forum post (admin only)
    """
    try:
        posts_collection = await get_forum_posts_collection()
        
        # Validate post ID
        try:
            ObjectId(post_id)
        except:
            raise HTTPException(status_code=400, detail="Invalid post ID")
        
        post = await posts_collection.find_one({"_id": post_id})
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        
        # Clean and validate update data
        allowed_updates = {}
        if "title" in update_data:
            allowed_updates["title"] = sanitize_text(update_data["title"], 200)
        if "content" in update_data:
            allowed_updates["content"] = sanitize_text(update_data["content"], 5000)
        if "is_pinned" in update_data:
            allowed_updates["isPinned"] = bool(update_data["is_pinned"])
        if "type" in update_data and update_data["type"] in ["announcement", "question", "update"]:
            allowed_updates["type"] = update_data["type"]
        
        if not allowed_updates:
            raise HTTPException(status_code=400, detail="No valid updates provided")
        
        allowed_updates["updatedAt"] = current_timestamp()
        
        await posts_collection.update_one(
            {"_id": post_id},
            {"$set": allowed_updates}
        )
        
        return create_response(message="Post updated successfully")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update post: {str(e)}"
        )


@app.delete("/posts/{post_id}")
async def delete_forum_post(
    post_id: str,
    admin_data: Dict[str, Any] = Depends(verify_admin)
):
    """
    Delete forum post and all its comments (admin only)
    """
    try:
        posts_collection = await get_forum_posts_collection()
        comments_collection = await get_forum_comments_collection()
        votes_collection = await get_user_votes_collection()
        
        # Validate post ID
        try:
            ObjectId(post_id)
        except:
            raise HTTPException(status_code=400, detail="Invalid post ID")
        
        post = await posts_collection.find_one({"_id": post_id})
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        
        # Delete all comments for this post
        await comments_collection.delete_many({"postId": post_id})
        
        # Delete all votes for this post and its comments
        await votes_collection.delete_many({"targetId": post_id})
        
        # Delete the post
        await posts_collection.delete_one({"_id": post_id})
        
        return create_response(message="Post and all related content deleted successfully")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete post: {str(e)}"
        )


@functions_framework.http
def main(request):
    """Cloud Function entry point"""
    return app(request.environ, lambda status, headers: None)