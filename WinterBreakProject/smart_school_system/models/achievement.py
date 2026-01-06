from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class AchievementRecord:
    student_id: str
    total_points: int = 0
    points_log: list[dict[str, Any]] = field(default_factory=list)
    badges: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "student_id": self.student_id,
            "total_points": int(self.total_points),
            "points_log": list(self.points_log),
            "badges": list(self.badges),
        }

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "AchievementRecord":
        return AchievementRecord(
            student_id=str(data["student_id"]),
            total_points=int(data.get("total_points", 0)),
            points_log=list(data.get("points_log", [])),
            badges=list(data.get("badges", [])),
        )

