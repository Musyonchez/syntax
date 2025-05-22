from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter

from app.routers.snippet import Query as SnippetQuery, Mutation as SnippetMutation
from app.routers.user import Query as UserQuery, Mutation as UserMutation
from app.routers.leaderboard import Query as LeaderboardQuery, Mutation as LeaderboardMutation

from app.routers import snippet, user, leaderboard  # REST routers

import strawberry

app = FastAPI(title="SyntaxMem API")

# Combine Snippet, User, and Leaderboard GraphQL schemas into one
@strawberry.type
class CombinedQuery(SnippetQuery, UserQuery, LeaderboardQuery):
    pass

@strawberry.type
class CombinedMutation(SnippetMutation, UserMutation, LeaderboardMutation):
    pass

# Create the combined schema
combined_schema = strawberry.Schema(query=CombinedQuery, mutation=CombinedMutation)

# Create a single GraphQL Router for combined schema
combined_graphql_app = GraphQLRouter(combined_schema)

# Include the combined GraphQL router at the /graphql endpoint
app.include_router(combined_graphql_app, prefix="/graphql")

# REST endpoints for snippets, users, and leaderboard
app.include_router(snippet.router, prefix="/snippets", tags=["Snippets"])
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(leaderboard.router, prefix="/leaderboard", tags=["Leaderboard"])

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to SyntaxMem API!"}
