from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints.content import router as content_router
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.category import router as category_router
from app.api.v1.endpoints.tag import router as tag_router
from app.api.v1.endpoints.reaction import router as reaction_router
from app.api.v1.endpoints.comment import router as comment_router

app = FastAPI()

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include API routers
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(content_router, prefix="/api/v1/content", tags=["content"])
app.include_router(category_router, prefix="/api/v1/categories", tags=["categories"])
app.include_router(tag_router, prefix="/api/v1/tags", tags=["tags"])
app.include_router(reaction_router, prefix="/api/v1/reactions", tags=["reactions"])
app.include_router(comment_router, prefix="/api/v1/comments", tags=["comments"])

@app.get("/")
async def root():
    return {"message": "Welcome to the API"} 