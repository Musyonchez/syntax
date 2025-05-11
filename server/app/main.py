
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter

from app.routers.snippet import Query as SnippetQuery, Mutation as SnippetMutation
from app.routers.user import Query as UserQuery, Mutation as UserMutation
from app.routers import snippet, user

import strawberry

app = FastAPI(title="SyntaxMem API")

# Combine Snippet and User GraphQL schemas into one
@strawberry.type
class CombinedQuery(SnippetQuery, UserQuery):
    pass

@strawberry.type
class CombinedMutation(SnippetMutation, UserMutation):
    pass

# Create the combined schema
combined_schema = strawberry.Schema(query=CombinedQuery, mutation=CombinedMutation)

# Create a single GraphQL Router for combined schema
combined_graphql_app = GraphQLRouter(combined_schema)

# Include the combined GraphQL router at the /graphql endpoint
app.include_router(combined_graphql_app, prefix="/graphql")

# REST endpoints for snippets and users
app.include_router(snippet.router, prefix="/snippets", tags=["Snippets"])
app.include_router(user.router, prefix="/users", tags=["Users"])

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































# # src/main.py

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from strawberry.fastapi import GraphQLRouter

# # from app.routers.snippet import Query as SnippetQuery, Mutation as SnippetMutation
# from app.routers.user import Query as UserQuery, Mutation as UserMutation
# from app.routers import snippet, user  # Add import for user router

# import strawberry

# app = FastAPI(title="SyntaxMem API")


# # # Combine Snippet and User GraphQL schemas into one
# # class CombinedQuery(SnippetQuery, UserQuery):
# #     pass


# # class CombinedMutation(SnippetMutation, UserMutation):
# #     pass


# # # Create the combined schema
# # combined_schema = strawberry.Schema(query=CombinedQuery, mutation=CombinedMutation)

# # # Create a single GraphQL Router for combined schema
# # combined_graphql_app = GraphQLRouter(combined_schema)

# # # Include the combined GraphQL router at the /graphql endpoint
# # app.include_router(combined_graphql_app, prefix="/graphql")

# # # Combine Snippet and User GraphQL schemas
# # snippet_schema = strawberry.Schema(query=SnippetQuery, mutation=SnippetMutation, subscription=None)
# user_schema = strawberry.Schema(query=UserQuery, mutation=UserMutation, subscription=None)

# # snippet_graphql_app = GraphQLRouter(snippet_schema)
# user_graphql_app = GraphQLRouter(user_schema)  # Add User GraphQL Router

# # app.include_router(snippet_graphql_app, prefix="/graphql/snippet")
# app.include_router(user_graphql_app, prefix="/graphql")  # User GraphQL route
# app.include_router(snippet.router, prefix="/snippets", tags=["Snippets"])
# app.include_router(
#     user.router, prefix="/users", tags=["Users"]
# )  # Users router for FastAPI

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# @app.get("/")
# def read_root():
#     return {"message": "Welcome to SyntaxMem API!"}
