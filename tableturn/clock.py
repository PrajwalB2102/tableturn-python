"""The clock is a dependency: every time-based rule reads it, so a test can move time instead of waiting."""

from datetime import datetime, timezone


def get_clock() -> datetime:
    return datetime.now(timezone.utc)
