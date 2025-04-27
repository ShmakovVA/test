from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.repositories.user import UserRepository
from app.services.user import UserService


async def db_session_dependency() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to provide a database session."""
    async with get_db_session() as session:
        yield session


async def user_service_dependency(db_session: AsyncSession) -> UserService:
    """Construct service."""
    users_repo: UserRepository = UserRepository(session=db_session)
    return UserService(users_repo)
