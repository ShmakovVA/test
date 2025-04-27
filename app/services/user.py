from datetime import datetime, timezone

from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.utils.security import get_password_hash


class UserService:
    """User service."""

    def __init__(self, users_repo: UserRepository):
        self.users_repo = users_repo

    async def list_users(self) -> list[UserResponse]:
        """List all users."""
        users = await self.users_repo.list()

        return [UserResponse(**user.to_dict(exclude=["password"])) for user in users]

    async def create_user(self, user_data: UserCreate) -> UserResponse:
        """Create a new user."""
        user = User(
            name=user_data.name,
            sername=user_data.sername,
            password=get_password_hash(user_data.password),
        )

        try:
            new_user = await self.users_repo.add(user)
        except Exception as e:
            await self.users_repo.session.rollback()
            raise e

        return UserResponse(**new_user.to_dict(exclude=["password"]))

    async def get_user(self, user_id: int) -> UserResponse:
        """Get a user by ID."""
        user = await self.users_repo.get(user_id)

        return UserResponse(**user.to_dict(exclude=["password"]))

    async def update_user(
        self, user_id: int, user_data: UserUpdate
    ) -> UserResponse | None:
        """Update a user."""
        user = await self.users_repo.get(user_id)
        if not user:
            return None

        if user_data.name:
            user.name = user_data.name
        if user_data.sername:
            user.sername = user_data.sername
        if user_data.password:
            user.password = get_password_hash(user_data.password)
        user.updated_at = datetime.now(tz=timezone.utc)

        try:
            updated_user = await self.users_repo.update(user)
        except Exception as e:
            await self.users_repo.session.rollback()
            raise e

        return UserResponse(**updated_user.to_dict(exclude=["password"]))

    async def delete_user(self, user_id: int) -> None:
        """Delete a user."""
        user = await self.users_repo.get(user_id)
        if not user:
            return None

        await self.users_repo.delete(user_id)

        return None
