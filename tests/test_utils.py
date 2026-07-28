from __future__ import annotations

from datetime import date, datetime

from src.utils import combine_date_and_time, parse_schedule_date


def test_parse_schedule_date() -> None:
    """Parse the timetable date format."""
    assert parse_schedule_date("17-Jul-26") == date(2026, 7, 17)


def test_combine_date_and_time() -> None:
    """Combine separate timetable date and time values."""
    assert combine_date_and_time(date(2026, 7, 17), "09:00") == datetime(2026, 7, 17, 9, 0)
