from __future__ import annotations

from datetime import date, datetime, time


def parse_date(date_str: str) -> date:
    try:
        return datetime.strptime(date_str.strip(), "%Y-%m-%d").date()
    except Exception as e:
        raise ValueError("Invalid date format. Expected YYYY-MM-DD.") from e


def parse_time(time_str: str) -> time:
    try:
        return datetime.strptime(time_str.strip(), "%H:%M").time()
    except Exception as e:
        raise ValueError("Invalid time format. Expected HH:MM (24h).") from e


def validate_time_range(start: time, end: time) -> None:
    if start >= end:
        raise ValueError("Invalid time range: start must be before end.")


def validate_nonempty(text: str, field: str) -> str:
    value = text.strip()
    if not value:
        raise ValueError(f"{field} cannot be empty.")
    return value


def validate_int_in_range(value: str, lo: int, hi: int) -> int:
    try:
        n = int(value.strip())
    except Exception as e:
        raise ValueError("Please enter a whole number.") from e
    if n < lo or n > hi:
        raise ValueError(f"Value must be between {lo} and {hi}.")
    return n
