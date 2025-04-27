"""User model definition."""

from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class User(Base):
    """User model for authentication and authorization."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, index=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(length=64), unique=True, index=True)
    sername: Mapped[str] = mapped_column(String(length=120))
    password: Mapped[str] = mapped_column(String(length=128))  # hashed password
    created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), default=func.current_timestamp()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), default=func.current_timestamp()
    )

    def __repr__(self) -> str:
        """String representation of the user."""
        return f"<User {self.name} {self.sername}>"
