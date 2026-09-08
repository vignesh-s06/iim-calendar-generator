from __future__ import annotations

from datetime import UTC, datetime
from zoneinfo import ZoneInfo

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
    assert event.decoded("dtstart") == datetime(2026, 7, 17, 9, 0, tzinfo=ZoneInfo("Asia/Kolkata"))
    assert event.decoded("dtend") == datetime(2026, 7, 17, 10, 30, tzinfo=ZoneInfo("Asia/Kolkata"))


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


def test_build_event_adds_alarm_for_subject() -> None:
    """Attach a VALARM to a subject event."""
    item = ScheduleItem(
        title="CFFM",
        start=datetime(2026, 7, 17, 9, 0),
        end=datetime(2026, 7, 17, 10, 30),
    )

    event = build_event(item)

    assert any(component.name == "VALARM" for component in event.subcomponents)


def test_build_event_adds_alarm_for_previously_excluded_subject() -> None:
    """Attach a reminder even for subjects outside the former allowlist."""
    item = ScheduleItem(
        title="SCM(S2)",
        start=datetime(2026, 7, 17, 9, 0),
        end=datetime(2026, 7, 17, 10, 30),
    )

    event = build_event(item)

    alarms = [component for component in event.subcomponents if component.name == "VALARM"]
    assert len(alarms) == 1
    assert alarms[0].decoded("trigger").total_seconds() == -15 * 60


def test_timezone_survives_ics_roundtrip_as_an_unambiguous_instant():
    item = ScheduleItem("CM", datetime(2026, 9, 8, 15), datetime(2026, 9, 8, 16, 30))
    serialized = build_calendar([item]).to_ical()
    assert b"DTSTART:20260908T093000Z" in serialized
    calendar = Calendar.from_ical(serialized)
    assert str(calendar["x-wr-timezone"]) == "Asia/Kolkata"
    event = calendar.walk("VEVENT")[0]
    assert event.decoded("dtstart") == datetime(2026, 9, 8, 9, 30, tzinfo=UTC)
    assert event.decoded("dtstart").astimezone(ZoneInfo("Asia/Kolkata")).hour == 15
    assert event.decoded("dtstamp").utcoffset().total_seconds() == 0
