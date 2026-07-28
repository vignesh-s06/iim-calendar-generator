from __future__ import annotations

from pathlib import Path
from typing import TypeAlias


TimeSlot: TypeAlias = tuple[str, str]

CALENDAR_NAME: str = "IIM Schedule"
CALENDAR_PRODID: str = "-//IIM Calendar Generator//EN"
CALENDAR_VERSION: str = "2.0"
LOCATION: str = "NAB G08"
REMINDER_MINUTES: int | None = 15
TIMEZONE: str | None = None
REMINDER_ACTION: str = "DISPLAY"
REMINDER_DESCRIPTION: str = "Reminder"

INPUT_FILENAME: Path = Path("input/schedule.pdf")
OUTPUT_FILENAME: Path = Path("output/iim-calendar.ics")

DATE_FORMAT: str = "%d-%b-%y"
TIMETABLE_END_MARKER: str = "Course Name"
IGNORED_SESSION_TOKENS: frozenset[str] = frozenset({"hrs", "venue", "date", "day"})

TIME_SLOTS: tuple[TimeSlot, ...] = (
    ("09:00", "10:30"),
    ("10:45", "12:15"),
    ("12:30", "14:00"),
    ("15:00", "16:30"),
    ("16:45", "18:15"),
    ("18:30", "20:00"),
    ("20:15", "21:45"),
)
