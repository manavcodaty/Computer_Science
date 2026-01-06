from __future__ import annotations

from datetime import date, datetime

from smart_school_system.core import storage
from smart_school_system.core.logger import log_event
from smart_school_system.models.achievement import AchievementRecord
from smart_school_system.models.user import User


def _get_record(
    achievements_by_student_id: dict[str, AchievementRecord], student_id: str
) -> AchievementRecord:
    rec = achievements_by_student_id.get(student_id)
    if rec is None:
        rec = AchievementRecord(student_id=student_id)
        achievements_by_student_id[student_id] = rec
    return rec


def award_points(
    teacher_user: User,
    student_id: str,
    points: int,
    category: str,
    note: str,
    achievements_by_student_id: dict[str, AchievementRecord],
) -> None:
    rec = _get_record(achievements_by_student_id, student_id)
    rec.total_points += int(points)
    rec.points_log.append(
        {
            "date": date.today().isoformat(),
            "points": int(points),
            "category": category,
            "note": note,
            "awarded_by": teacher_user.id,
        }
    )
    log_event("points_awarded", user=teacher_user)
    storage.save_json(
        str(storage.data_path("achievements.json")),
        {sid: r.to_dict() for sid, r in achievements_by_student_id.items()},
    )


def award_badge(
    teacher_user: User,
    student_id: str,
    badge_name: str,
    achievements_by_student_id: dict[str, AchievementRecord],
    allowed_badges: set[str],
) -> None:
    if badge_name not in allowed_badges:
        raise ValueError("Badge name not in allowed list.")
    rec = _get_record(achievements_by_student_id, student_id)
    rec.badges.append(
        {
            "badge_name": badge_name,
            "date": date.today().isoformat(),
            "awarded_by": teacher_user.id,
        }
    )
    log_event("badge_awarded", user=teacher_user)
    storage.save_json(
        str(storage.data_path("achievements.json")),
        {sid: r.to_dict() for sid, r in achievements_by_student_id.items()},
    )


def view_student_profile(
    user: User,
    achievements_by_student_id: dict[str, AchievementRecord],
    users_by_id: dict[str, User],
) -> None:
    target_id = user.id
    rec = achievements_by_student_id.get(target_id)
    print(f"\nProfile: {user.username}")
    if rec is None:
        print("Total points: 0")
        print("Badges: (none)")
        print("Points history: (none)")
        return
    print(f"Total points: {rec.total_points}")
    print("Badges:")
    if not rec.badges:
        print("  (none)")
    else:
        for b in rec.badges:
            print(f"  - {b['badge_name']} ({b['date']})")
    print("Points history:")
    if not rec.points_log:
        print("  (none)")
    else:
        for entry in rec.points_log[-20:]:
            print(
                f"  - {entry['date']}: {entry['points']} [{entry['category']}] {entry['note']}"
            )


def leaderboard(
    achievements_by_student_id: dict[str, AchievementRecord], top_n: int = 10
) -> list[tuple[str, int]]:
    rows = [(sid, rec.total_points)
            for sid, rec in achievements_by_student_id.items()]
    rows.sort(key=lambda r: (-r[1], r[0]))
    if not rows:
        return []
    if len(rows) <= top_n:
        return rows
    cutoff_points = rows[top_n - 1][1]
    return [r for r in rows if r[1] >= cutoff_points]


def print_leaderboard(
    rows: list[tuple[str, int]], users_by_id: dict[str, User]
) -> None:
    last_points = None
    rank = 0
    for i, (sid, points) in enumerate(rows, start=1):
        if last_points != points:
            rank = i
            last_points = points
        name = users_by_id.get(sid).username if sid in users_by_id else sid
        print(f"{rank:>2}. {name:<12} {points} pts")
