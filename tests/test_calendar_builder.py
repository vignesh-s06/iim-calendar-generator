from __future__ import annotations

from datetime import datetime

from icalendar import Calendar

from src.calendar_builder import build_calendar, build_event
from src.config import CALENDAR_NAME
from src.utils import ScheduleItem


def test_build_event_creates_calendar_event() -> None:
    """Build an iCalendar VEVENT from a schedule item."""
    item = ScheduleItem(
        title="SCM(S2)",
        start=datetime(2026, 7, 17, 9, 0),
        end=datetime(2026, 7, 17, 10, 30),
    )

    event = build_event(item)

    assert event.name == "VEVENT"
    assert str(event.get("summary")) == "SCM(S2)"
    assert event.decoded("dtstart") == datetime(2026, 7, 17, 9, 0)
    assert event.decoded("dtend") == datetime(2026, 7, 17, 10, 30)


def test_build_calendar_adds_events_and_name() -> None:
    """Build a calendar containing all provided schedule events."""
    items = [
        ScheduleItem("SCM(S2)", datetime(2026, 7, 17, 9, 0), datetime(2026, 7, 17, 10, 30)),
        ScheduleItem("GTBL(S2)", datetime(2026, 7, 17, 10, 45), datetime(2026, 7, 17, 12, 15)),
    ]

    calendar = build_calendar(items)
    parsed_calendar = Calendar.from_ical(calendar.to_ical())
    events = [component for component in parsed_calendar.walk() if component.name == "VEVENT"]

    assert str(parsed_calendar.get("x-wr-calname")) == CALENDAR_NAME
    assert len(events) == 2
