from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from app.models.user import User


class UserRepository(SQLAlchemyAsyncRepository[User]):  # type: ignore
    """User repository."""

    model_type = User
