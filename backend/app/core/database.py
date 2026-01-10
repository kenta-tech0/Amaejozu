"""
Database connection and session management
非同期MySQLデータベース接続を管理
"""

import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

# Base class for models (must be defined before importing config)
Base = declarative_base()

# Only create engine if not running from Alembic
# Alembic will create its own sync engine
if "ALEMBIC_CONFIG" not in os.environ:
    from app.core.config import settings

    # Create async engine
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        pool_pre_ping=True,
        pool_recycle=3600,
    )

    # Create async session factory
    AsyncSessionLocal = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )
else:
    # Placeholder for Alembic
    engine = None
    AsyncSessionLocal = None


async def get_db():
    """
    Dependency function to get database session
    FastAPI依存性注入用のデータベースセッション取得関数
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """Initialize database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
