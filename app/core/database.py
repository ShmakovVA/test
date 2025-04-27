"""Database configuration and session management."""

from contextlib import asynccontextmanager
from typing import AsyncContextManager, AsyncGenerator, Callable

from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)
from sqlalchemy.pool import NullPool

from app.core.config import settings

# Create async engine
engine: AsyncEngine = create_async_engine(
    str(settings.DATABASE_URL),
    echo=settings.DATABASE_ECHO,
    poolclass=NullPool,
    pool_pre_ping=True,
)

# Create async session factory
async_session_factory: Callable[[], AsyncContextManager[AsyncSession]] = (
    async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )
)


@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get a database session."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


@asynccontextmanager
async def provide_transaction(
    db_session: AsyncSession,
) -> AsyncGenerator[AsyncSession, None]:
    """Provide a transactional scope around a series of operations."""
    async with db_session.begin():
        try:
            yield db_session
        except Exception:
            await db_session.rollback()
            raise
