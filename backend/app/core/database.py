"""
Jukeyman Autonomous Media Station (JAMS) - Database Connection
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from app.core.config import settings

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
    echo=settings.DEBUG,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_pre_ping=True,
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Base class for models
Base = declarative_base()


# Dependency to get DB session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency function to get database session.
    Yields an async session and closes it after use.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# Context manager for database operations
@asynccontextmanager
async def get_db_context():
    """
    Context manager for database operations.
    Usage:
        async with get_db_context() as db:
            result = await db.execute(query)
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# Set tenant context for Row-Level Security
async def set_tenant_context(session: AsyncSession, tenant_id: str, user_id: str = None):
    """
    Set PostgreSQL session variables for RLS (Row-Level Security).
    This must be called before any queries that use RLS policies.
    """
    await session.execute(
        f"SET LOCAL app.current_tenant_id = '{tenant_id}'"
    )
    if user_id:
        await session.execute(
            f"SET LOCAL app.current_user_id = '{user_id}'"
        )


# Initialize database
async def init_db():
    """
    Initialize database connection.
    Create tables if they don't exist.
    """
    async with engine.begin() as conn:
        # Import all models here to register them
        from app.models import tenant, user, generation, product, order
        
        # Create tables (in production, use Alembic migrations)
        # await conn.run_sync(Base.metadata.create_all)
        pass


# Close database connection
async def close_db():
    """
    Close database connection pool.
    """
    await engine.dispose()

