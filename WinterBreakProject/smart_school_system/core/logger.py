from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


def _log_path() -> Path:
    base = Path(__file__).resolve().parents[1]
    logs_dir = base / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    return logs_dir / "app.log"


def log_event(event: str, user=None) -> None:
    ts = datetime.now().isoformat(timespec="seconds")
    who = ""
    if user is not None:
        who = f" user={getattr(user, 'username', '?')}({getattr(user, 'role', '?')})"
    with _log_path().open("a", encoding="utf-8") as f:
        f.write(f"{ts} event={event}{who}\n")


def log_exception(event: str, trace: str, user=None) -> None:
    ts = datetime.now().isoformat(timespec="seconds")
    who = ""
    if user is not None:
        who = f" user={getattr(user, 'username', '?')}({getattr(user, 'role', '?')})"
    with _log_path().open("a", encoding="utf-8") as f:
        f.write(f"{ts} event={event}{who}\n{trace}\n")
