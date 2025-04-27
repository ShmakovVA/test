from typing import Any

from advanced_alchemy.base import orm_registry
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all models"""

    registry = orm_registry

    def to_dict(self, exclude: list[str] | None = None) -> dict[str, Any]:
        if exclude is None:
            exclude = []

        return {
            field.name: getattr(self, field.name)
            for field in self.__table__.c
            if field.name not in exclude
        }
