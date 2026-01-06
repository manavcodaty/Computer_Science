from __future__ import annotations

import uuid
from collections import deque
from datetime import date, datetime, time

from smart_school_system.core import storage
from smart_school_system.core.logger import log_event
from smart_school_system.core.ui import safe_input
from smart_school_system.models.booking import Booking
from smart_school_system.models.room import Room
from smart_school_system.models.user import User


def list_rooms(rooms: dict[str, Room]) -> None:
    print("\nRooms:")
    for r in rooms.values():
        features = ", ".join(r.features) if r.features else "no features listed"
        print(f"- {r.id}: {r.name} [{r.type}] cap={r.capacity} ({features})")


def _slot_key(room_id: str, booking_date: date, start: time, end: time) -> str:
    return f"{room_id}:{booking_date.isoformat()}:{start.strftime('%H:%M')}-{end.strftime('%H:%M')}"


def _time_tuple(t: time) -> tuple[int, int]:
    return (t.hour, t.minute)


def has_conflict(room_id: str, booking_date: date, start: time, end: time, bookings: list[Booking]) -> bool:
    start_m = _time_tuple(start)
    end_m = _time_tuple(end)
    for b in bookings:
        if b.room_id != room_id or b.date != booking_date:
            continue
        if b.status not in {"approved", "pending"}:
            continue
        b_start = _time_tuple(b.start_time)
        b_end = _time_tuple(b.end_time)
        # Conflict if (start < existing_end) and (end > existing_start)
        if start_m < b_end and end_m > b_start:
            return True
    return False


def find_available_rooms(
    booking_date: date,
    start: time,
    end: time,
    rooms: dict[str, Room],
    bookings: list[Booking],
) -> list[Room]:
    available: list[Room] = []
    for room in rooms.values():
        if not has_conflict(room.id, booking_date, start, end, bookings):
            available.append(room)
    return available


def enqueue_waitlist(slot_key: str, user_id: str, waitlists: dict[str, deque[str]]) -> None:
    q = waitlists.setdefault(slot_key, deque())
    if user_id in q:
        return
    q.append(user_id)
    _persist(bookings=None, waitlists=waitlists)


def _persist(bookings: list[Booking] | None, waitlists: dict[str, deque[str]] | None) -> None:
    if bookings is not None:
        storage.save_json(str(storage.data_path("bookings.json")), [b.to_dict() for b in bookings])
    if waitlists is not None:
        storage.save_json(str(storage.data_path("waitlists.json")), {k: list(q) for k, q in waitlists.items()})


def _parse_slot_key(slot_key: str) -> tuple[str, date, time, time] | None:
    try:
        room_id, date_s, range_s = slot_key.split(":", 2)
        start_s, end_s = range_s.split("-", 1)
        from smart_school_system.core.validation import parse_date, parse_time

        return room_id, parse_date(date_s), parse_time(start_s), parse_time(end_s)
    except Exception:
        return None


def _promote_waitlists_for_room_date(
    room_id: str,
    booking_date: date,
    bookings: list[Booking],
    waitlists: dict[str, deque[str]],
    approval_required: bool,
) -> None:
    candidates: list[tuple[time, str]] = []
    for key in waitlists.keys():
        parsed = _parse_slot_key(key)
        if not parsed:
            continue
        rid, d, start, _end = parsed
        if rid == room_id and d == booking_date:
            candidates.append((start, key))
    candidates.sort(key=lambda t: _time_tuple(t[0]))

    for _start, key in candidates:
        parsed = _parse_slot_key(key)
        if not parsed:
            continue
        rid, d, start, end = parsed
        if rid != room_id or d != booking_date:
            continue
        if has_conflict(room_id, booking_date, start, end, bookings):
            continue
        q = waitlists.get(key)
        if not q:
            continue
        next_user_id = q.popleft()
        if not q:
            waitlists.pop(key, None)
        new_status = "pending" if approval_required else "approved"
        bookings.append(
            Booking(
                id=str(uuid.uuid4()),
                room_id=room_id,
                user_id=next_user_id,
                date=booking_date,
                start_time=start,
                end_time=end,
                purpose="(auto from waitlist)",
                status=new_status,
                created_at=datetime.now(),
            )
        )
        log_event("waitlist_promoted")


def request_booking(
    user: User,
    room_id: str,
    booking_date: date,
    start: time,
    end: time,
    purpose: str,
    bookings: list[Booking],
    waitlists: dict[str, deque[str]],
    approval_required: bool = True,
    on_conflict: str = "prompt",  # prompt|waitlist|cancel
) -> Booking | None:
    if has_conflict(room_id, booking_date, start, end, bookings):
        slot = _slot_key(room_id, booking_date, start, end)
        print("That slot conflicts with an existing booking.")
        if on_conflict == "waitlist":
            join = "y"
        elif on_conflict == "cancel":
            join = "n"
        else:
            raw = safe_input("Join waitlist for this slot? (y/n or 'q' to cancel): ")
            if raw is None:
                return None
            join = raw.strip().lower()
            if join == "q":
                return None
        if join == "y":
            enqueue_waitlist(slot, user.id, waitlists)
            log_event("waitlist_joined", user=user)
            print("Added to waitlist.")
            _persist(bookings=bookings, waitlists=waitlists)
        return None

    status = "pending" if approval_required else "approved"
    booking = Booking(
        id=str(uuid.uuid4()),
        room_id=room_id,
        user_id=user.id,
        date=booking_date,
        start_time=start,
        end_time=end,
        purpose=purpose,
        status=status,
        created_at=datetime.now(),
    )
    bookings.append(booking)
    log_event("booking_requested", user=user)
    _persist(bookings=bookings, waitlists=waitlists)
    return booking


def list_user_future_bookings(user: User, bookings: list[Booking], rooms: dict[str, Room]) -> list[Booking]:
    today = date.today()
    future = [
        b
        for b in bookings
        if b.user_id == user.id
        and (b.date > today or (b.date == today and _time_tuple(b.end_time) > _time_tuple(datetime.now().time())))
        and b.status in {"approved", "pending"}
    ]
    if not future:
        print("\n(no future bookings)")
        return []
    print("\nYour future bookings:")
    for b in future:
        room_name = rooms.get(b.room_id).name if b.room_id in rooms else b.room_id
        print(
            f"- {b.id} [{b.status}] {b.date.isoformat()} {b.start_time.strftime('%H:%M')}-{b.end_time.strftime('%H:%M')} "
            f"{room_name} purpose={b.purpose}"
        )
    return future


def cancel_booking(
    user: User,
    booking_id: str,
    bookings: list[Booking],
    waitlists: dict[str, deque[str]],
    approval_required: bool = True,
) -> bool:
    idx = next((i for i, b in enumerate(bookings) if b.id == booking_id), None)
    if idx is None:
        print("Booking not found.")
        return False
    booking = bookings[idx]
    if booking.user_id != user.id and user.role != "admin":
        print("You can only cancel your own bookings (admin can cancel any).")
        return False
    if booking.date < date.today():
        print("Cannot cancel past bookings.")
        return False

    removed = bookings.pop(idx)
    log_event("booking_cancelled", user=user)
    print("Booking cancelled.")

    before = len(bookings)
    _promote_waitlists_for_room_date(removed.room_id, removed.date, bookings, waitlists, approval_required)
    if len(bookings) > before:
        print("A waitlisted user was promoted into an available slot.")
    _persist(bookings=bookings, waitlists=waitlists)
    return True


def admin_review_bookings(
    admin_user: User,
    bookings: list[Booking],
    rooms: dict[str, Room],
    users: dict[str, User],
    waitlists: dict[str, deque[str]] | None = None,
    approval_required: bool = True,
    demo_auto: bool = False,
) -> None:
    pending = [b for b in bookings if b.status == "pending"]
    if not pending:
        print("\n(no pending bookings)")
        return
    print("\nPending bookings:")
    for b in pending:
        room = rooms.get(b.room_id)
        user = users.get(b.user_id)
        room_label = room.name if room else b.room_id
        user_label = user.username if user else b.user_id
        print(
            f"- {b.id} {b.date.isoformat()} {b.start_time.strftime('%H:%M')}-{b.end_time.strftime('%H:%M')} "
            f"room={room_label} by={user_label} purpose={b.purpose}"
        )
    for b in pending:
        if demo_auto:
            decision = "a"
        else:
            raw = safe_input(f"Approve/Decline booking {b.id}? (a/d/skip): ")
            if raw is None:
                return
            decision = raw.strip().lower()
        if decision == "a":
            b.status = "approved"
            log_event("booking_approved", user=admin_user)
        elif decision == "d":
            b.status = "declined"
            log_event("booking_declined", user=admin_user)
            if waitlists is not None:
                _promote_waitlists_for_room_date(b.room_id, b.date, bookings, waitlists, approval_required)
        else:
            continue
    print("Review complete.")
    _persist(bookings=bookings, waitlists=waitlists)
