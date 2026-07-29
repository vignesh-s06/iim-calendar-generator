from __future__ import annotations

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from icalendar import Alarm, Calendar, Event

from src.config import (
    CALENDAR_NAME,
    CALENDAR_PRODID,
    CALENDAR_VERSION,
    LOCATION,
    REMINDER_ACTION,
    REMINDER_DESCRIPTION,
    REMINDER_MINUTES,
    REMINDER_SUBJECTS,
    TIMEZONE,
)
from src.utils import ScheduleItem


def build_calendar(
    items: list[ScheduleItem],
    calendar_name: str = CALENDAR_NAME,
    location: str = LOCATION,
    timezone: str | None = TIMEZONE,
    reminder_minutes: int | None = REMINDER_MINUTES,
    reminder_subjects: frozenset[str] = REMINDER_SUBJECTS,
) -> Calendar:
    """Build an iCalendar document from parsed schedule items."""
    calendar = Calendar()
    calendar.add("prodid", CALENDAR_PRODID)
    calendar.add("version", CALENDAR_VERSION)
    calendar.add("x-wr-calname", calendar_name)

    for item in items:
        calendar.add_component(build_event(item, location, timezone, reminder_minutes, reminder_subjects))

    return calendar


def build_event(
    item: ScheduleItem,
    location: str = LOCATION,
    timezone: str | None = TIMEZONE,
    reminder_minutes: int | None = REMINDER_MINUTES,
    reminder_subjects: frozenset[str] = REMINDER_SUBJECTS,
) -> Event:
    """Build one iCalendar event from a parsed schedule item."""
    event = Event()
    event.add("summary", item.title)
    event.add("dtstart", _apply_timezone(item.start, timezone))
    event.add("dtend", _apply_timezone(item.end, timezone))
    event.add("dtstamp", current_timestamp(timezone))

    if location:
        event.add("location", location)

    if reminder_minutes is not None and item.title in reminder_subjects:
        event.add_component(_build_alarm(reminder_minutes))

    return event


def current_timestamp(timezone: str | None = TIMEZONE) -> datetime:
    """Return the timestamp used when creating calendar events."""
    if timezone is None:
        return datetime.now()

    return datetime.now(ZoneInfo(timezone))


def _apply_timezone(value: datetime, timezone: str | None) -> datetime:
    if timezone is None:
        return value

    return value.replace(tzinfo=ZoneInfo(timezone))


def _build_alarm(reminder_minutes: int) -> Alarm:
    alarm = Alarm()
    alarm.add("action", REMINDER_ACTION)
    alarm.add("description", REMINDER_DESCRIPTION)
    alarm.add("trigger", timedelta(minutes=-reminder_minutes))
    return alarm
