from __future__ import annotations

import re
from pathlib import Path

from pypdf import PdfReader

from src.config import IGNORED_SESSION_TOKENS, TIMETABLE_END_MARKER, TIME_SLOTS
from src.utils import ScheduleItem, combine_date_and_time, parse_schedule_date


DATE_PATTERN = re.compile(r"\d{1,2}-[A-Za-z]{3}-\d{2}")
WEEKDAY_PATTERN = re.compile(
    r"^(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\s*",
    re.IGNORECASE,
)
SESSION_PATTERN = re.compile(
    r"Comm\. Workshop|INDEPENDENCE DAY|MILAD-UN-NABI|End Term|"
    r"[A-Z0-9&]+(?:\([A-Z0-9]+\))?",
    re.IGNORECASE,
)


def parse_pdf_schedule(pdf_path: Path) -> list[ScheduleItem]:
    """Parse schedule events from a PDF file."""
    return parse_schedule_text(extract_text(pdf_path))


def extract_text(pdf_path: Path) -> str:
    """Extract text from every page in a PDF file."""
    reader = PdfReader(str(pdf_path))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def parse_schedule_text(text: str) -> list[ScheduleItem]:
    """Parse schedule events from extracted timetable text."""
    timetable_text = text.split(TIMETABLE_END_MARKER, 1)[0]
    date_matches: list[re.Match[str]] = list(DATE_PATTERN.finditer(timetable_text))
    items: list[ScheduleItem] = []

    for index, match in enumerate(date_matches):
        next_start = date_matches[index + 1].start() if index + 1 < len(date_matches) else len(timetable_text)
        row_text = timetable_text[match.end() : next_start].strip()
        row_text = WEEKDAY_PATTERN.sub("", row_text).strip()
        schedule_date = parse_schedule_date(match.group(0))

        sessions = [session.strip() for session in SESSION_PATTERN.findall(row_text)]
        sessions = [session for session in sessions if session.lower() not in IGNORED_SESSION_TOKENS]

        for slot, title in zip(TIME_SLOTS, sessions):
            start_time, end_time = slot
            items.append(
                ScheduleItem(
                    title=normalize_title(title),
                    start=combine_date_and_time(schedule_date, start_time),
                    end=combine_date_and_time(schedule_date, end_time),
                )
            )

    return items


def normalize_title(title: str) -> str:
    """Normalize whitespace in a parsed session title."""
    return " ".join(title.split())
