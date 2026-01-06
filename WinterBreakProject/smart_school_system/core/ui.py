from __future__ import annotations


def safe_input(prompt: str) -> str | None:
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print()
        return None

