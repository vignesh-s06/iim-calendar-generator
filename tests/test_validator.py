from __future__ import annotations

from datetime import datetime

from icalendar import Calendar, Event

from src.calendar_builder import build_calendar
from src.utils import ScheduleItem
from src.validator import validate_calendar


def test_validate_calendar_passes_complete_events() -> None:
    """Pass validation for complete events with location and reminder."""
    calendar = build_calendar(
        [ScheduleItem("SCM(S2)", datetime(2026, 7, 17, 9, 0), datetime(2026, 7, 17, 10, 30))],
        location="NAB G08",
        reminder_minutes=15,
    )

    report = validate_calendar(calendar)

    assert report.event_count == 1
    assert report.duplicate_events == 0
    assert report.invalid_dates == 0
    assert report.invalid_time_ranges == 0
    assert report.missing_summary == 0
    assert report.missing_dtstart == 0
    assert report.missing_dtend == 0
    assert report.missing_location == 0
    assert report.missing_valarm == 0
    assert report.passed


def test_validate_calendar_counts_missing_fields_and_invalid_ranges() -> None:
    """Report missing fields and invalid time ranges."""
    calendar = Calendar()
    event = Event()
    event.add("summary", "")
    event.add("dtstart", datetime(2026, 7, 17, 10, 30))
    event.add("dtend", datetime(2026, 7, 17, 9, 0))
    calendar.add_component(event)

    report = validate_calendar(calendar)

    assert report.event_count == 1
    assert report.invalid_time_ranges == 1
    assert report.missing_summary == 1
    assert report.missing_location == 1
    assert report.missing_valarm == 1
    assert not report.passed


def test_validate_calendar_counts_duplicate_events() -> None:
    """Report duplicate events with matching summary, start, end, and location."""
    item = ScheduleItem("SCM(S2)", datetime(2026, 7, 17, 9, 0), datetime(2026, 7, 17, 10, 30))
    calendar = build_calendar([item, item], location="NAB G08", reminder_minutes=15)

    report = validate_calendar(calendar)

    assert report.duplicate_events == 1
    assert not report.passed
