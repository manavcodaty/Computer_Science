from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class Room:
    id: str
    name: str
    type: str
    capacity: int
    features: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "capacity": self.capacity,
            "features": list(self.features),
        }

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "Room":
        return Room(
            id=str(data["id"]),
            name=str(data["name"]),
            type=str(data["type"]),
            capacity=int(data["capacity"]),
            features=list(data.get("features", [])),
        )
