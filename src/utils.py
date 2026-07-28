from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time

from src.config import DATE_FORMAT


@dataclass(frozen=True)
class ScheduleItem:
    """A parsed class or schedule entry ready for calendar generation."""

    title: str
    start: datetime
    end: datetime


def parse_schedule_date(value: str) -> date:
    """Parse a schedule date from the timetable date format."""
    return datetime.strptime(value, DATE_FORMAT).date()


def combine_date_and_time(schedule_date: date, value: str) -> datetime:
    """Combine a schedule date and time string into a datetime."""
    parsed_time = time.fromisoformat(value)
    return datetime.combine(schedule_date, parsed_time)
