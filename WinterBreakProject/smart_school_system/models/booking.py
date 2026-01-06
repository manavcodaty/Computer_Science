from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time
from typing import Any

from smart_school_system.core.validation import parse_date, parse_time


@dataclass(slots=True)
class Booking:
    id: str
    room_id: str
    user_id: str
    date: date
    start_time: time
    end_time: time
    purpose: str
    status: str  # approved|pending|declined
    created_at: datetime

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "room_id": self.room_id,
            "user_id": self.user_id,
            "date": self.date.isoformat(),
            "start_time": self.start_time.strftime("%H:%M"),
            "end_time": self.end_time.strftime("%H:%M"),
            "purpose": self.purpose,
            "status": self.status,
            "created_at": self.created_at.isoformat(timespec="seconds"),
        }

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "Booking":
        return Booking(
            id=str(data["id"]),
            room_id=str(data["room_id"]),
            user_id=str(data["user_id"]),
            date=parse_date(str(data["date"])),
            start_time=parse_time(str(data["start_time"])),
            end_time=parse_time(str(data["end_time"])),
            purpose=str(data.get("purpose", "")),
            status=str(data.get("status", "pending")),
            created_at=datetime.fromisoformat(str(data["created_at"])),
        )
