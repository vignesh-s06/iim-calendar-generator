from __future__ import annotations

from icalendar import Calendar

from src.calendar_builder import build_calendar
from src.config import INPUT_FILENAME, OUTPUT_FILENAME
from src.parser import parse_pdf_schedule


def test_generate_calendar_from_input_pdf() -> None:
    """Generate the output ICS file from the real input schedule PDF."""
    schedule_items = parse_pdf_schedule(INPUT_FILENAME)
    OUTPUT_FILENAME.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILENAME.write_bytes(build_calendar(schedule_items).to_ical())

    assert OUTPUT_FILENAME.exists()

    calendar = Calendar.from_ical(OUTPUT_FILENAME.read_bytes())
    events = [component for component in calendar.walk() if component.name == "VEVENT"]

    assert len(events) >= 1
