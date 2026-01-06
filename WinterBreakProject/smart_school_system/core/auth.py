from __future__ import annotations

import hashlib

from smart_school_system.core.logger import log_event
from smart_school_system.core.ui import safe_input
from smart_school_system.models.user import User


def _hash_pin(pin: str) -> str:
    return hashlib.sha256(pin.encode("utf-8")).hexdigest()


def login(users_by_id: dict[str, User]) -> User | None:
    print("=== Smart School System ===")
    while True:
        username = safe_input("Username (or 'q' to quit): ")
        if username is None:
            return None
        username = username.strip()
        if username.lower() == "q":
            return None
        pin = safe_input("PIN (or 'q' to quit): ")
        if pin is None:
            return None
        pin = pin.strip()
        if pin.lower() == "q":
            return None

        for user in users_by_id.values():
            if user.username == username:
                # Prototype support: accept plain pin field if present.
                if user.pin_hash and user.pin_hash == _hash_pin(pin):
                    return user
                if user.pin and user.pin == pin:
                    return user
        print("Invalid username or PIN.\n")
        log_event("login_failed")


def require_role(user: User, allowed: set[str]) -> bool:
    if user.role in allowed:
        return True
    print(f"Access denied: requires one of {sorted(allowed)}.")
    log_event("access_denied", user=user)
    return False
