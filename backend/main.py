"""
FastAPI application entry point.
Initializes database, registers routes, and configures middleware.
"""
import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from database import init_db
from routers import survey

# Initialize database
try:
    init_db()
except Exception as e:
    print(f"✗ Database initialization failed: {e}")
    print("Make sure PostgreSQL is running and the connection string is correct.")
    sys.exit(1)

# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="Mini Survey Application API"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(survey.router)


@app.get("/")
def read_root():
    """Health check endpoint."""
    return {
        "status": "ok",
        "message": "Mini Survey API is running",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
