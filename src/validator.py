from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any

from icalendar import Calendar


@dataclass(frozen=True)
class ValidationReport:
    """Summary of calendar validation results."""

    event_count: int
    duplicate_events: int
    invalid_dates: int
    invalid_time_ranges: int
    missing_summary: int
    missing_dtstart: int
    missing_dtend: int
    missing_location: int
    missing_valarm: int

    @property
    def passed(self) -> bool:
        """Return whether the calendar passed validation."""
        return (
            self.event_count > 0
            and self.duplicate_events == 0
            and self.invalid_dates == 0
            and self.invalid_time_ranges == 0
            and self.missing_summary == 0
            and self.missing_dtstart == 0
            and self.missing_dtend == 0
            and self.missing_location == 0
            and self.missing_valarm == 0
        )


class CalendarValidationError(Exception):
    """Raised when an ICS calendar cannot be validated."""


def validate_calendar_file(calendar_path: Path) -> ValidationReport:
    """Validate an existing ICS calendar file."""
    if not calendar_path.exists():
        raise CalendarValidationError(f"Missing calendar file: {calendar_path}")

    if not calendar_path.is_file():
        raise CalendarValidationError(f"Invalid calendar path: {calendar_path} is not a file")

    try:
        calendar = Calendar.from_ical(calendar_path.read_bytes())
    except ValueError as error:
        raise CalendarValidationError(f"Invalid calendar file: {calendar_path}") from error

    return validate_calendar(calendar)


def validate_calendar(calendar: Calendar) -> ValidationReport:
    """Validate an iCalendar object and return a report."""
    events = [component for component in calendar.walk() if component.name == "VEVENT"]
    duplicate_events = count_duplicate_events(events)

    invalid_dates = 0
    invalid_time_ranges = 0
    missing_summary = 0
    missing_dtstart = 0
    missing_dtend = 0
    missing_location = 0
    missing_valarm = 0

    for event in events:
        if not event.get("summary"):
            missing_summary += 1

        if not event.get("dtstart"):
            missing_dtstart += 1

        if not event.get("dtend"):
            missing_dtend += 1

        if not event.get("location"):
            missing_location += 1

        if not any(component.name == "VALARM" for component in event.subcomponents):
            missing_valarm += 1

        try:
            start = event.decoded("dtstart")
            end = event.decoded("dtend")
        except (KeyError, ValueError, TypeError):
            invalid_dates += 1
            continue

        if not isinstance(start, datetime) or not isinstance(end, datetime):
            invalid_dates += 1
            continue

        if end <= start:
            invalid_time_ranges += 1

    return ValidationReport(
        event_count=len(events),
        duplicate_events=duplicate_events,
        invalid_dates=invalid_dates,
        invalid_time_ranges=invalid_time_ranges,
        missing_summary=missing_summary,
        missing_dtstart=missing_dtstart,
        missing_dtend=missing_dtend,
        missing_location=missing_location,
        missing_valarm=missing_valarm,
    )


def count_duplicate_events(events: list[Any]) -> int:
    """Count duplicate VEVENT entries by summary, start, end, and location."""
    seen: set[tuple[str, date | datetime | None, date | datetime | None, str]] = set()
    duplicates = 0

    for event in events:
        key = (
            str(event.get("summary") or ""),
            safe_decoded(event, "dtstart"),
            safe_decoded(event, "dtend"),
            str(event.get("location") or ""),
        )

        if key in seen:
            duplicates += 1
            continue

        seen.add(key)

    return duplicates


def safe_decoded(event: Any, field_name: str) -> date | datetime | None:
    """Decode a calendar event field without raising validation errors."""
    try:
        value = event.decoded(field_name)
    except (KeyError, ValueError, TypeError):
        return None

    if isinstance(value, date):
        return value

    return None
