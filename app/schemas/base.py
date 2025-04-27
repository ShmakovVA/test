from msgspec import Struct
from msgspec.structs import asdict


class StructBase(Struct, kw_only=True):
    """Base schema for Any model."""

    def to_dict(self) -> dict:
        return asdict(self)
