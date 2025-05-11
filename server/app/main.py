from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter

from app.routers.snippet import Query as SnippetQuery, Mutation as SnippetMutation
from app.routers import snippet

import strawberry

app = FastAPI(title="SyntaxMem API")


schema = strawberry.Schema(query=SnippetQuery, mutation=SnippetMutation)
graphql_app = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql")
app.include_router(snippet.router, prefix="/snippets", tags=["Snippets"])

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



