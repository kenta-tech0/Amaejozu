"""
FastAPI Application Entry Point
メインアプリケーション
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="化粧品の価格を自動で監視し、価格変動を通知するWebアプリケーション",
    version="0.1.0",
    debug=settings.DEBUG,
)

# CORS middleware
origins = settings.CORS_ORIGINS.split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint - health check"""
    return {
        "message": "Amaejozu API is running",
        "version": "0.1.0",
        "status": "healthy"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected"
    }


@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    print("🚀 Starting Amaejozu API...")

@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    print("👋 Shutting down Amaejozu API...")
