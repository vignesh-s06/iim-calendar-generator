from __future__ import annotations

from datetime import datetime

from src.parser import normalize_title, parse_schedule_text


def test_parse_schedule_text_extracts_sessions_from_timetable_rows() -> None:
    """Parse session entries from compact IIM timetable text."""
    text = (
        "Indian Institute of Management Shillong"
        "DateDay9:00-10:30 hrs10:45-12:15 hrs"
        "17-Jul-26Friday SCM(S2) GTBL(S2)"
        "18-Jul-26Saturday BIA PM"
        "Course Name Course Code Area Credits/Sessions"
    )

    items = parse_schedule_text(text)

    assert [item.title for item in items] == ["SCM(S2)", "GTBL(S2)", "BIA", "PM"]
    assert items[0].start == datetime(2026, 7, 17, 9, 0)
    assert items[0].end == datetime(2026, 7, 17, 10, 30)
    assert items[2].start == datetime(2026, 7, 18, 9, 0)


def test_parse_schedule_text_ignores_empty_days() -> None:
    """Return no events for timetable rows without sessions."""
    text = "30-Aug-26Sunday31-Aug-26Monday End Term Course Name"

    items = parse_schedule_text(text)

    assert [item.title for item in items] == ["End Term"]


def test_normalize_title_collapses_whitespace() -> None:
    """Normalize whitespace in parsed course names."""
    assert normalize_title("Comm.   Workshop") == "Comm. Workshop"
