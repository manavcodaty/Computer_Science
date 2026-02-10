from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Any

from smart_school_system.core.validation import parse_date


@dataclass(slots=True)
class Announcement:
    id: str
    title: str
    body: str
    audience: str  # all|students|teachers
    created_by: str
    created_at: datetime
    expires_on: date | None
    status: str  # active|archived

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "audience": self.audience,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat(timespec="seconds"),
            "expires_on": self.expires_on.isoformat() if self.expires_on else None,
            "status": self.status,
        }

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "Announcement":
        expires = data.get("expires_on")
        return Announcement(
            id=str(data["id"]),
            title=str(data["title"]),
            body=str(data["body"]),
            audience=str(data.get("audience", "all")),
            created_by=str(data.get("created_by", "")),
            created_at=datetime.fromisoformat(str(data["created_at"])),
            expires_on=parse_date(expires) if expires else None,
            status=str(data.get("status", "active")),
        )
