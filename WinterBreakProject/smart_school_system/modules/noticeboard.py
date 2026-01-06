from __future__ import annotations

import copy
import uuid
from datetime import date, datetime

from smart_school_system.core.logger import log_event
from smart_school_system.core import storage
from smart_school_system.models.announcement import Announcement
from smart_school_system.models.user import User


def create_announcement(
    user: User,
    title: str,
    body: str,
    audience: str,
    expires_on: date | None,
    announcements: list[Announcement],
) -> Announcement:
    ann = Announcement(
        id=str(uuid.uuid4()),
        title=title,
        body=body,
        audience=audience,
        created_by=user.id,
        created_at=datetime.now(),
        expires_on=expires_on,
        status="active",
    )
    announcements.append(ann)
    log_event("announcement_created", user=user)
    storage.save_json(str(storage.data_path("announcements.json")), [a.to_dict() for a in announcements])
    return ann


def _is_visible_to(user: User, ann: Announcement) -> bool:
    if ann.status != "active":
        return False
    if ann.expires_on and ann.expires_on < date.today():
        return False
    if user.role == "admin":
        return True
    if ann.audience == "all":
        return True
    if ann.audience == "students":
        return user.role == "student"
    if ann.audience == "teachers":
        return user.role == "teacher"
    return False


def list_announcements(user: User, announcements: list[Announcement], include_archived: bool = False) -> list[Announcement]:
    out: list[Announcement] = []
    for ann in announcements:
        if include_archived:
            out.append(ann)
        else:
            if _is_visible_to(user, ann):
                out.append(ann)
    out.sort(key=lambda a: a.created_at, reverse=True)
    return out


def archive_announcement(user: User, announcement_id: str, announcements: list[Announcement], undo_stack: list[dict]) -> bool:
    ann = next((a for a in announcements if a.id == announcement_id), None)
    if ann is None:
        print("Announcement not found.")
        return False
    if ann.status == "archived":
        print("Announcement is already archived.")
        return False
    undo_stack.append(copy.deepcopy(ann.to_dict()))  # stack push
    ann.status = "archived"
    log_event("announcement_archived", user=user)
    storage.save_json(str(storage.data_path("announcements.json")), [a.to_dict() for a in announcements])
    print("Archived.")
    return True


def undo_last_archive(user: User, announcements: list[Announcement], undo_stack: list[dict]) -> bool:
    if not undo_stack:
        print("Nothing to undo.")
        return False
    snapshot = undo_stack.pop()  # stack pop
    ann_id = snapshot["id"]
    current = next((a for a in announcements if a.id == ann_id), None)
    if current is None:
        announcements.append(Announcement.from_dict(snapshot))
    else:
        current.status = "active"
    log_event("announcement_unarchived", user=user)
    storage.save_json(str(storage.data_path("announcements.json")), [a.to_dict() for a in announcements])
    print("Undo complete.")
    return True
