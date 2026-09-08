from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
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
    TIMEZONE,
)
from src.utils import ScheduleItem


def build_calendar(
    items: list[ScheduleItem],
    calendar_name: str = CALENDAR_NAME,
    location: str = LOCATION,
    timezone: str | None = TIMEZONE,
    reminder_minutes: int | None = REMINDER_MINUTES,
) -> Calendar:
    """Build an iCalendar document from parsed schedule items."""
    calendar = Calendar()
    calendar.add("prodid", CALENDAR_PRODID)
    calendar.add("version", CALENDAR_VERSION)
    calendar.add("x-wr-calname", calendar_name)
    if timezone:
        calendar.add("x-wr-timezone", timezone)

    for item in items:
        calendar.add_component(build_event(item, location, timezone, reminder_minutes))

    return calendar


def build_event(
    item: ScheduleItem,
    location: str = LOCATION,
    timezone: str | None = TIMEZONE,
    reminder_minutes: int | None = REMINDER_MINUTES,
) -> Event:
    """Build one iCalendar event from a parsed schedule item."""
    event = Event()
    event.add("summary", item.title)
    event.add("dtstart", _apply_timezone(item.start, timezone))
    event.add("dtend", _apply_timezone(item.end, timezone))
    event.add("dtstamp", current_timestamp(timezone))

    if location:
        event.add("location", location)

    if reminder_minutes is not None:
        event.add_component(_build_alarm(reminder_minutes))

    return event


def current_timestamp(timezone: str | None = TIMEZONE) -> datetime:
    """Use UTC for the calendar creation timestamp."""
    return datetime.now(UTC)


def _apply_timezone(value: date | datetime, timezone: str | None) -> date | datetime:
    if timezone is None or not isinstance(value, datetime):
        return value

    # UTC timestamps are unambiguous without requiring a VTIMEZONE component.
    localized = value.replace(tzinfo=ZoneInfo(timezone)) if value.tzinfo is None else value
    return localized.astimezone(UTC)


def _build_alarm(reminder_minutes: int) -> Alarm:
    alarm = Alarm()
    alarm.add("action", REMINDER_ACTION)
    alarm.add("description", REMINDER_DESCRIPTION)
    alarm.add("trigger", timedelta(minutes=-reminder_minutes))
    return alarm
