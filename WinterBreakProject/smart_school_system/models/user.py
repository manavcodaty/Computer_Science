from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class User:
    id: str
    username: str
    pin_hash: str | None
    pin: str | None
    role: str  # student|teacher|admin

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "username": self.username,
            "pin_hash": self.pin_hash,
            "pin": self.pin,
            "role": self.role,
        }

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "User":
        return User(
            id=str(data["id"]),
            username=str(data["username"]),
            pin_hash=data.get("pin_hash"),
            pin=data.get("pin"),
            role=str(data["role"]),
        )

