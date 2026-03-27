from __future__ import annotations

import argparse
import sys
import traceback
from datetime import date, datetime
from pathlib import Path

from smart_school_system.core import auth, logger, storage, validation
from smart_school_system.core.ui import safe_input
from smart_school_system.modules import achievements, noticeboard, room_booking


def _pause() -> None:
    safe_input("\nPress Enter to continue...")


def _prompt_menu(title: str, options: list[tuple[str, str]]) -> str:
    while True:
        print(f"\n=== {title} ===")
        for key, label in options:
            print(f"{key}) {label}")
        raw = safe_input("> ")
        if raw is None:
            return "q"
        choice = raw.strip().lower()
        if choice == "q":
            return "q"
        valid = {k for k, _ in options}
        if choice in valid:
            return choice
        print("Invalid choice. Try again, or enter 'q' to go back.")


def _prompt_text(label: str) -> str | None:
    while True:
        raw = safe_input(f"{label} (or 'q' to go back): ")
        if raw is None:
            return None
        raw = raw.strip()
        if raw.lower() == "q":
            return None
        try:
            return validation.validate_nonempty(raw, label)
        except ValueError as e:
            print(e)


def _prompt_date(label: str) -> date | None:
    while True:
        raw = safe_input(f"{label} YYYY-MM-DD (or 'q' to go back): ")
        if raw is None:
            return None
        raw = raw.strip()
        if raw.lower() == "q":
            return None
        try:
            return validation.parse_date(raw)
        except ValueError as e:
            print(e)


def _prompt_time(label: str) -> datetime.time | None:
    while True:
        raw = safe_input(f"{label} HH:MM 24h (or 'q' to go back): ")
        if raw is None:
            return None
        raw = raw.strip()
        if raw.lower() == "q":
            return None
        try:
            return validation.parse_time(raw)
        except ValueError as e:
            print(e)


def _prompt_int(label: str, lo: int, hi: int) -> int | None:
    while True:
        raw = safe_input(f"{label} ({lo}..{hi}) (or 'q' to go back): ")
        if raw is None:
            return None
        raw = raw.strip()
        if raw.lower() == "q":
            return None
        try:
            return validation.validate_int_in_range(raw, lo, hi)
        except ValueError as e:
            print(e)


def _load_state() -> storage.AppState:
    storage.ensure_data_files()
    return storage.load_state()


def _save_state(state: storage.AppState) -> None:
    storage.save_state(state)


def _handle_room_booking(user, state: storage.AppState) -> None:
    while True:
        choice = _prompt_menu(
            "Room Booking",
            [
                ("1", "List rooms"),
                ("2", "Search availability"),
                ("3", "Request booking"),
                ("4", "Cancel my booking"),
                ("q", "Back"),
            ],
        )
        if choice == "q":
            return
        if choice == "1":
            room_booking.list_rooms(state.rooms_by_id)
            _pause()
        elif choice == "2":
            booking_date = _prompt_date("Date")
            if booking_date is None:
                continue
            start = _prompt_time("Start time")
            if start is None:
                continue
            end = _prompt_time("End time")
            if end is None:
                continue
            try:
                validation.validate_time_range(start, end)
            except ValueError as e:
                print(e)
                continue
            available = room_booking.find_available_rooms(
                booking_date,
                start,
                end,
                state.rooms_by_id,
                state.bookings,
            )
            print("\nAvailable rooms:")
            if not available:
                print("  (none)")
            for r in available:
                print(
                    f"- {r.id}: {r.name} ({r.type}), cap {r.capacity}, {', '.join(r.features)}"
                )
            _pause()
        elif choice == "3":
            if not auth.require_role(user, {"student", "teacher", "admin"}):
                continue
            room_booking.list_rooms(state.rooms_by_id)
            room_id = _prompt_text("Room ID")
            if room_id is None:
                continue
            if room_id not in state.rooms_by_id:
                print("Unknown room id.")
                continue
            booking_date = _prompt_date("Date")
            if booking_date is None:
                continue
            start = _prompt_time("Start time")
            if start is None:
                continue
            end = _prompt_time("End time")
            if end is None:
                continue
            try:
                validation.validate_time_range(start, end)
            except ValueError as e:
                print(e)
                continue
            purpose = _prompt_text("Purpose")
            if purpose is None:
                continue
            created = room_booking.request_booking(
                user=user,
                room_id=room_id,
                booking_date=booking_date,
                start=start,
                end=end,
                purpose=purpose,
                bookings=state.bookings,
                waitlists=state.waitlists,
                approval_required=state.config["booking_approval_required"],
            )
            if created is None:
                print("No booking created.")
            else:
                print(
                    f"Booking {created.id} created with status '{created.status}'.")
            _save_state(state)
            _pause()
        elif choice == "4":
            future = room_booking.list_user_future_bookings(
                user, state.bookings, state.rooms_by_id
            )
            if not future:
                _pause()
                continue
            booking_id = _prompt_text("Booking ID to cancel")
            if booking_id is None:
                continue
            changed = room_booking.cancel_booking(
                user=user,
                booking_id=booking_id,
                bookings=state.bookings,
                waitlists=state.waitlists,
                approval_required=state.config["booking_approval_required"],
            )
            if changed:
                _save_state(state)
            _pause()


def _handle_noticeboard(user, state: storage.AppState) -> None:
    undo_stack = state.undo_archive_stack
    while True:
        choice = _prompt_menu(
            "Digital Noticeboard",
            [
                ("1", "View announcements"),
                ("2", "Post announcement (teacher/admin)"),
                ("3", "Archive announcement (teacher/admin)"),
                ("4", "Undo last archive (teacher/admin)"),
                ("q", "Back"),
            ],
        )
        if choice == "q":
            return
        if choice == "1":
            items = noticeboard.list_announcements(user, state.announcements)
            if not items:
                print("\n(no announcements)")
            else:
                print()
                for a in items:
                    expires = a.expires_on.isoformat() if a.expires_on else "never"
                    print(
                        f"- {a.id} [{a.audience}] (expires {expires}) {a.title}\n  {a.body}"
                    )
            _pause()
        elif choice == "2":
            if not auth.require_role(user, {"teacher", "admin"}):
                continue
            title = _prompt_text("Title")
            if title is None:
                continue
            body = _prompt_text("Body")
            if body is None:
                continue
            audience = _prompt_menu(
                "Audience",
                [("1", "all"), ("2", "students"),
                 ("3", "teachers"), ("q", "Back")],
            )
            if audience == "q":
                continue
            audience_value = {"1": "all", "2": "students",
                              "3": "teachers"}[audience]
            while True:
                raw = input(
                    "Expiry date YYYY-MM-DD (blank for none, 'q' to go back): "
                ).strip()
                if raw.lower() == "q":
                    expires = "__back__"
                    break
                if raw == "":
                    expires = None
                    break
                try:
                    expires = validation.parse_date(raw)
                    break
                except ValueError as e:
                    print(e)
            if expires == "__back__":
                continue
            created = noticeboard.create_announcement(
                user=user,
                title=title,
                body=body,
                audience=audience_value,
                expires_on=expires,
                announcements=state.announcements,
            )
            _save_state(state)
            print(f"Announcement {created.id} posted.")
            _pause()
        elif choice == "3":
            if not auth.require_role(user, {"teacher", "admin"}):
                continue
            active = noticeboard.list_announcements(
                user, state.announcements, include_archived=True
            )
            if not active:
                print("\n(no announcements)")
                _pause()
                continue
            print("\nAnnouncements:")
            for a in active:
                print(f"- {a.id} [{a.status}] {a.title}")
            ann_id = _prompt_text("Announcement ID to archive")
            if ann_id is None:
                continue
            ok = noticeboard.archive_announcement(
                user, ann_id, state.announcements, undo_stack
            )
            if ok:
                _save_state(state)
            _pause()
        elif choice == "4":
            if not auth.require_role(user, {"teacher", "admin"}):
                continue
            ok = noticeboard.undo_last_archive(
                user, state.announcements, undo_stack)
            if ok:
                _save_state(state)
            _pause()


def _handle_achievements(user, state: storage.AppState) -> None:
    while True:
        choice = _prompt_menu(
            "Student Achievement Tracker",
            [
                ("1", "View my profile"),
                ("2", "View leaderboard"),
                ("3", "Award points (teacher/admin)"),
                ("4", "Award badge (teacher/admin)"),
                ("q", "Back"),
            ],
        )
        if choice == "q":
            return
        if choice == "1":
            achievements.view_student_profile(
                user, state.achievements_by_student_id, state.users_by_id
            )
            _pause()
        elif choice == "2":
            top_n = _prompt_int("Show top N", 1, 50)
            if top_n is None:
                continue
            rows = achievements.leaderboard(
                state.achievements_by_student_id, top_n=top_n
            )
            if not rows:
                print("\n(no achievement records)")
            else:
                print("\nLeaderboard:")
                achievements.print_leaderboard(rows, state.users_by_id)
            _pause()
        elif choice == "3":
            if not auth.require_role(user, {"teacher", "admin"}):
                continue
            student = _prompt_text("Student username")
            if student is None:
                continue
            student_id = storage.find_user_id_by_username(
                state.users_by_id, student)
            if not student_id:
                print("Unknown student username.")
                _pause()
                continue
            points = _prompt_int(
                "Points", state.config["points_min"], state.config["points_max"]
            )
            if points is None:
                continue
            category = _prompt_text("Category")
            if category is None:
                continue
            note = _prompt_text("Note")
            if note is None:
                continue
            achievements.award_points(
                teacher_user=user,
                student_id=student_id,
                points=points,
                category=category,
                note=note,
                achievements_by_student_id=state.achievements_by_student_id,
            )
            _save_state(state)
            print("Points awarded.")
            _pause()
        elif choice == "4":
            if not auth.require_role(user, {"teacher", "admin"}):
                continue
            student = _prompt_text("Student username")
            if student is None:
                continue
            student_id = storage.find_user_id_by_username(
                state.users_by_id, student)
            if not student_id:
                print("Unknown student username.")
                _pause()
                continue
            print("\nAllowed badges:")
            for b in state.allowed_badges:
                print(f"- {b}")
            badge_name = _prompt_text("Badge name")
            if badge_name is None:
                continue
            achievements.award_badge(
                teacher_user=user,
                student_id=student_id,
                badge_name=badge_name,
                achievements_by_student_id=state.achievements_by_student_id,
                allowed_badges=set(state.allowed_badges),
            )
            _save_state(state)
            print("Badge awarded.")
            _pause()


def _handle_admin_tools(user, state: storage.AppState) -> None:
    if not auth.require_role(user, {"admin"}):
        return
    while True:
        choice = _prompt_menu(
            "Admin Tools",
            [
                ("1", "Review pending bookings"),
                ("2", "List users"),
                ("3", "Create user"),
                ("4", "Add room"),
                ("q", "Back"),
            ],
        )
        if choice == "q":
            return
        if choice == "1":
            room_booking.admin_review_bookings(
                user,
                state.bookings,
                state.rooms_by_id,
                state.users_by_id,
                waitlists=state.waitlists,
                approval_required=state.config["booking_approval_required"],
            )
            _save_state(state)
            _pause()
        elif choice == "2":
            print("\nUsers:")
            for u in state.users_by_id.values():
                print(f"- {u.username} ({u.role}) id={u.id}")
            _pause()
        elif choice == "3":
            username = _prompt_text("Username")
            if username is None:
                continue
            pin = _prompt_text("PIN")
            if pin is None:
                continue
            role_choice = _prompt_menu(
                "Role",
                [("1", "student"), ("2", "teacher"),
                 ("3", "admin"), ("q", "Back")],
            )
            if role_choice == "q":
                continue
            role = {"1": "student", "2": "teacher", "3": "admin"}[role_choice]
            try:
                storage.create_user(
                    state, username=username, pin=pin, role=role)
            except ValueError as e:
                print(e)
            else:
                _save_state(state)
                print("User created.")
            _pause()
        elif choice == "4":
            name = _prompt_text("Room name")
            if name is None:
                continue
            room_type = _prompt_text("Room type")
            if room_type is None:
                continue
            capacity = _prompt_int("Capacity", 1, 500)
            if capacity is None:
                continue
            features_raw = _prompt_text("Features (comma-separated)")
            if features_raw is None:
                continue
            features = [f.strip()
                        for f in features_raw.split(",") if f.strip()]
            storage.add_room(
                state,
                name=name,
                room_type=room_type,
                capacity=capacity,
                features=features,
            )
            _save_state(state)
            print("Room added.")
            _pause()


def run_cli() -> int:
    state = _load_state()
    user = auth.login(state.users_by_id)
    if user is None:
        print("Login cancelled.")
        return 0

    logger.log_event("login_success", user=user)
    while True:
        try:
            options = [
                ("1", "Room Booking"),
                ("2", "Noticeboard"),
                ("3", "Achievements"),
            ]
            if user.role == "admin":
                options.append(("4", "Admin Tools"))
            options.extend(
                [("s", "Save"), ("x", "Save & Exit"), ("q", "Exit (no save)")]
            )

            choice = _prompt_menu(
                f"Main Menu ({user.username} / {user.role})", options)
            if choice == "1":
                _handle_room_booking(user, state)
            elif choice == "2":
                _handle_noticeboard(user, state)
            elif choice == "3":
                _handle_achievements(user, state)
            elif choice == "4" and user.role == "admin":
                _handle_admin_tools(user, state)
            elif choice == "s":
                _save_state(state)
                print("Saved.")
            elif choice == "x":
                _save_state(state)
                print("Saved. Bye.")
                return 0
            elif choice == "q":
                print("Bye.")
                return 0
        except Exception:
            logger.log_exception("ui_error", traceback.format_exc(), user=user)
            print("Something went wrong. Details were logged.")
            _pause()


def run_demo() -> int:
    state = _load_state()
    users = state.users_by_id
    admin = next(u for u in users.values() if u.username == "admin")
    teacher = next(u for u in users.values() if u.username == "teacher1")
    student1 = next(u for u in users.values() if u.username == "student1")
    student2 = next(u for u in users.values() if u.username == "student2")
    room_id = next(iter(state.rooms_by_id.keys()))

    logger.log_event("demo_started")

    today = date.today()
    start = validation.parse_time("10:00")
    end = validation.parse_time("11:00")

    room_booking.request_booking(
        user=student1,
        room_id=room_id,
        booking_date=today,
        start=start,
        end=end,
        purpose="Study session",
        bookings=state.bookings,
        waitlists=state.waitlists,
        approval_required=True,
    )
    room_booking.request_booking(
        user=student2,
        room_id=room_id,
        booking_date=today,
        start=start,
        end=end,
        purpose="Group work",
        bookings=state.bookings,
        waitlists=state.waitlists,
        approval_required=True,
        on_conflict="waitlist",
    )
    room_booking.admin_review_bookings(
        admin,
        state.bookings,
        state.rooms_by_id,
        state.users_by_id,
        waitlists=state.waitlists,
        approval_required=True,
        demo_auto=True,
    )
    b1 = next(
        (
            b
            for b in state.bookings
            if b.user_id == student1.id and b.room_id == room_id and b.date == today
        ),
        None,
    )
    if b1 is not None:
        room_booking.cancel_booking(
            admin, b1.id, state.bookings, state.waitlists, approval_required=True
        )

    noticeboard.create_announcement(
        user=teacher,
        title="Welcome back!",
        body="Check the noticeboard for updates.",
        audience="all",
        expires_on=None,
        announcements=state.announcements,
    )
    if state.announcements:
        noticeboard.archive_announcement(
            teacher,
            state.announcements[0].id,
            state.announcements,
            state.undo_archive_stack,
        )
        noticeboard.undo_last_archive(
            teacher, state.announcements, state.undo_archive_stack
        )

    achievements.award_points(
        teacher_user=teacher,
        student_id=student1.id,
        points=10,
        category="participation",
        note="Great contributions in class.",
        achievements_by_student_id=state.achievements_by_student_id,
    )
    achievements.award_badge(
        teacher_user=teacher,
        student_id=student1.id,
        badge_name=state.allowed_badges[0],
        achievements_by_student_id=state.achievements_by_student_id,
        allowed_badges=set(state.allowed_badges),
    )

    _save_state(state)
    print("Demo complete. Check logs in smart_school_system/logs/app.log")
    return 0


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="smart-school-system")
    parser.add_argument(
        "--demo", action="store_true", help="run a short scripted demo scenario"
    )
    args = parser.parse_args(argv)

    try:
        code = run_demo() if args.demo else run_cli()
        raise SystemExit(code)
    except SystemExit:
        raise
    except (KeyboardInterrupt, EOFError):
        print("\nInterrupted.")
        raise SystemExit(130)
    except Exception:
        logger.log_exception("fatal_error", traceback.format_exc())
        print(
            "\nA fatal error occurred. Details logged to smart_school_system/logs/app.log"
        )
        raise
