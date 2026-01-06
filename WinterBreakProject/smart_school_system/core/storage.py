from __future__ import annotations

import hashlib
import json
import uuid
from collections import deque
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from smart_school_system.core.logger import log_event, log_exception
from smart_school_system.models.achievement import AchievementRecord
from smart_school_system.models.announcement import Announcement
from smart_school_system.models.booking import Booking
from smart_school_system.models.room import Room
from smart_school_system.models.user import User


def _base_dir() -> Path:
    return Path(__file__).resolve().parents[1]


def _data_dir() -> Path:
    d = _base_dir() / "data"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _hash_pin(pin: str) -> str:
    return hashlib.sha256(pin.encode("utf-8")).hexdigest()


def load_json(path: str, default: Any) -> Any:
    p = Path(path)
    if not p.exists():
        return default
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        ts = datetime.now().strftime("%Y%m%d%H%M%S")
        corrupt_path = p.with_name(f"{p.stem}.corrupt.{ts}{p.suffix}")
        try:
            p.rename(corrupt_path)
        except Exception:
            pass
        log_exception(f"json_corrupt:{p.name}", trace=_safe_trace())
        save_json(str(p), default)
        return default
    except Exception:
        log_exception(f"json_load_failed:{p.name}", trace=_safe_trace())
        return default


def save_json(path: str, data: Any) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def _safe_trace() -> str:
    import traceback

    return traceback.format_exc()


def ensure_data_files() -> None:
    d = _data_dir()

    files: dict[str, Any] = {
        "users.json": [],
        "rooms.json": [],
        "bookings.json": [],
        "waitlists.json": {},
        "announcements.json": [],
        "achievements.json": {},
        "badges.json": ["Star Helper", "Math Whiz", "Perfect Attendance"],
    }

    for name, default in files.items():
        path = d / name
        if not path.exists():
            save_json(str(path), default)

    # Seed users/rooms if empty (first run).
    users_path = d / "users.json"
    rooms_path = d / "rooms.json"
    users_raw = load_json(str(users_path), [])
    rooms_raw = load_json(str(rooms_path), [])
    if not users_raw:
        seed_users = [
            User(id=str(uuid.uuid4()), username="admin", pin_hash=_hash_pin("1234"), pin=None, role="admin"),
            User(id=str(uuid.uuid4()), username="teacher1", pin_hash=_hash_pin("1234"), pin=None, role="teacher"),
            User(id=str(uuid.uuid4()), username="student1", pin_hash=_hash_pin("1234"), pin=None, role="student"),
            User(id=str(uuid.uuid4()), username="student2", pin_hash=_hash_pin("1234"), pin=None, role="student"),
        ]
        save_json(str(users_path), [u.to_dict() for u in seed_users])
        log_event("seed_users_created")
    if not rooms_raw:
        seed_rooms = [
            Room(
                id="R101",
                name="Room 101",
                type="classroom",
                capacity=30,
                features=["projector", "whiteboard"],
            ),
            Room(
                id="LAB1",
                name="Computer Lab 1",
                type="lab",
                capacity=24,
                features=["pc", "3d-printer"],
            ),
            Room(
                id="STUDIO",
                name="Art Studio",
                type="studio",
                capacity=18,
                features=["easels", "sink"],
            ),
            Room(
                id="MUSIC",
                name="Music Room",
                type="studio",
                capacity=15,
                features=["piano", "sound-system"],
            ),
            Room(
                id="HALL",
                name="Assembly Hall",
                type="hall",
                capacity=200,
                features=["stage", "pa-system"],
            ),
        ]
        save_json(str(rooms_path), [r.to_dict() for r in seed_rooms])
        log_event("seed_rooms_created")


def data_path(filename: str) -> Path:
    return _data_dir() / filename


@dataclass
class AppState:
    users_by_id: dict[str, User]
    rooms_by_id: dict[str, Room]
    bookings: list[Booking]
    waitlists: dict[str, deque[str]]
    announcements: list[Announcement]
    achievements_by_student_id: dict[str, AchievementRecord]
    allowed_badges: list[str]
    undo_archive_stack: list[dict[str, Any]]
    config: dict[str, Any]


def load_state() -> AppState:
    d = _data_dir()
    users_raw = load_json(str(d / "users.json"), [])
    rooms_raw = load_json(str(d / "rooms.json"), [])
    bookings_raw = load_json(str(d / "bookings.json"), [])
    waitlists_raw = load_json(str(d / "waitlists.json"), {})
    announcements_raw = load_json(str(d / "announcements.json"), [])
    achievements_raw = load_json(str(d / "achievements.json"), {})
    badges_raw = load_json(str(d / "badges.json"), ["Star Helper", "Math Whiz", "Perfect Attendance"])

    users = {u["id"]: User.from_dict(u) for u in users_raw}
    rooms = {r["id"]: Room.from_dict(r) for r in rooms_raw}
    bookings = [Booking.from_dict(b) for b in bookings_raw]
    waitlists = {k: deque(v) for k, v in waitlists_raw.items()}
    announcements = [Announcement.from_dict(a) for a in announcements_raw]
    achievements = {sid: AchievementRecord.from_dict(rec) for sid, rec in achievements_raw.items()}

    return AppState(
        users_by_id=users,
        rooms_by_id=rooms,
        bookings=bookings,
        waitlists=waitlists,
        announcements=announcements,
        achievements_by_student_id=achievements,
        allowed_badges=list(badges_raw),
        undo_archive_stack=[],
        config={
            "booking_approval_required": True,
            "points_min": -20,
            "points_max": 50,
        },
    )


def save_state(state: AppState) -> None:
    d = _data_dir()
    save_json(str(d / "users.json"), [u.to_dict() for u in state.users_by_id.values()])
    save_json(str(d / "rooms.json"), [r.to_dict() for r in state.rooms_by_id.values()])
    save_json(str(d / "bookings.json"), [b.to_dict() for b in state.bookings])
    save_json(str(d / "waitlists.json"), {k: list(q) for k, q in state.waitlists.items()})
    save_json(str(d / "announcements.json"), [a.to_dict() for a in state.announcements])
    save_json(
        str(d / "achievements.json"),
        {sid: rec.to_dict() for sid, rec in state.achievements_by_student_id.items()},
    )
    save_json(str(d / "badges.json"), list(state.allowed_badges))
    log_event("state_saved")


def find_user_id_by_username(users_by_id: dict[str, User], username: str) -> str | None:
    for u in users_by_id.values():
        if u.username == username:
            return u.id
    return None


def create_user(state: AppState, username: str, pin: str, role: str) -> None:
    if role not in {"student", "teacher", "admin"}:
        raise ValueError("Invalid role.")
    if any(u.username == username for u in state.users_by_id.values()):
        raise ValueError("Username already exists.")
    u = User(id=str(uuid.uuid4()), username=username, pin_hash=_hash_pin(pin), pin=None, role=role)
    state.users_by_id[u.id] = u
    log_event("user_created")


def add_room(state: AppState, name: str, room_type: str, capacity: int, features: list[str]) -> None:
    rid = f"R{uuid.uuid4().hex[:6].upper()}"
    r = Room(id=rid, name=name, type=room_type, capacity=capacity, features=features)
    state.rooms_by_id[r.id] = r
    log_event("room_added")
