"""
FastAPI Application Entry Point
英語スピーキング練習アプリ
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select

from app.core.config import settings
from app.core.database import engine, AsyncSessionLocal, Base
from app.models import Scenario, PracticeSession, Message
from app.api.scenarios import router as scenarios_router
from app.api.sessions import router as sessions_router
from app.services.scenario_seed import SCENARIOS


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown"""
    # Startup
    print("Starting SpeakEasy API...")

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Seed scenarios if empty
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Scenario).limit(1))
        if not result.scalar_one_or_none():
            for data in SCENARIOS:
                scenario = Scenario(**data)
                session.add(scenario)
            await session.commit()
            print(f"Seeded {len(SCENARIOS)} scenarios")

    yield

    # Shutdown
    print("Shutting down SpeakEasy API...")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="英語スピーキング練習アプリ - シナリオベースのAI英会話",
    version="1.0.0",
    debug=settings.DEBUG,
    lifespan=lifespan,
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

# Register routers
app.include_router(scenarios_router)
app.include_router(sessions_router)


@app.get("/")
async def root():
    """Root endpoint - health check"""
    return {
        "message": "SpeakEasy API is running",
        "version": "1.0.0",
        "status": "healthy",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "database": "connected"}
