from collections import Counter
from datetime import date, datetime

import pytest

from src.config import INPUT_FILENAME
from src.parser import parse_schedule
from src.calendar_builder import build_calendar
from src.validator import validate_calendar
from icalendar import Calendar


def test_current_workbook_preserves_empty_slots_and_late_classes():
    items = parse_schedule(INPUT_FILENAME)
    first_day = [item for item in items if isinstance(item.start, datetime) and item.start.date() == date(2026, 9, 8)]
    assert [(item.title, item.start.hour, item.start.minute) for item in first_day] == [("CM", 15, 0), ("SOM", 18, 30)]
    assert first_day[0].end == datetime(2026, 9, 8, 16, 30)
    assert any(item.title == "CM" and item.start == datetime(2026, 9, 28, 20, 15) for item in items)


def test_current_workbook_contains_only_term_iv_with_complete_course_counts():
    items = parse_schedule(INPUT_FILENAME)
    classes = [item for item in items if isinstance(item.start, datetime)]
    assert Counter(item.title for item in classes) == {
        "CM": 20, "SOM": 20, "MI": 20, "PABF": 20,
        "ESLCA": 20, "MACR(S2)": 20, "SSLT(S2)": 20,
        "SM": 20, "OR": 10, "LCM": 10,
    }
    assert min(item.start for item in classes) == datetime(2026, 9, 8, 15, 0)
    assert max(item.end for item in classes) == datetime(2026, 11, 27, 14, 0)


def test_merged_holidays_and_exam_period_survive_calendar_roundtrip():
    items = parse_schedule(INPUT_FILENAME)
    all_day = [item for item in items if not isinstance(item.start, datetime)]
    assert len(all_day) == 8
    assert all_day[0].title == "GANESH CHATURTHI / VINAYAK CHATURTHI"
    assert all_day[-1].title == "END TERM EXAMINATION"
    assert all_day[-1].start == date(2026, 11, 30)
    assert all_day[-1].end == date(2026, 12, 6)
    calendar = Calendar.from_ical(build_calendar(items).to_ical())
    report = validate_calendar(calendar)
    assert report.passed
    assert report.event_count == 188
    exam = next(event for event in calendar.walk("VEVENT") if str(event["summary"]) == "END TERM EXAMINATION")
    assert exam.decoded("dtstart") == date(2026, 11, 30)
    assert exam.decoded("dtend") == date(2026, 12, 6)


def test_unsupported_input_format_is_rejected():
    with pytest.raises(ValueError, match="Unsupported timetable format"):
        parse_schedule(INPUT_FILENAME.with_suffix(".csv"))
