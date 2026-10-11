from collections import Counter
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from icalendar import Calendar

from src.cli import main
from src.validator import validate_calendar


def test_generate_calendar_from_input_workbook(tmp_path):
    """The production CLI keeps the inclusive cutoff and latest timetable changes."""
    output = tmp_path / "calendar.ics"
    assert main(["--output", str(output)]) == 0
    calendar = Calendar.from_ical(output.read_bytes())
    assert validate_calendar(calendar).passed
    events = calendar.walk("VEVENT")
    classes = [e for e in events if isinstance(e.decoded("dtstart"), datetime)]
    all_day = [e for e in events if not isinstance(e.decoded("dtstart"), datetime)]
    assert len(classes) == 108
    assert len(all_day) == 6
    assert Counter(str(e["summary"]) for e in classes) == {
        "VbN": 6, "SOM": 16, "OR": 5, "MACR(S2)": 14, "PABF": 12,
        "LCM": 5, "SMKTG": 9, "SSLT(S2)": 11, "CM": 10, "MI": 10, "ESLCA": 10,
    }
    india = ZoneInfo("Asia/Kolkata")
    for event in events:
        start = event.decoded("dtstart")
        local_date = start.astimezone(india).date() if isinstance(start, datetime) else start
        assert local_date >= date(2026, 10, 12)
        assert any(a.name == "VALARM" and a.decoded("trigger") == timedelta(minutes=-15)
                   for a in event.subcomponents)
    first_day = [e for e in classes if e.decoded("dtstart").astimezone(india).date() == date(2026, 10, 12)]
    assert [(str(e["summary"]), e.decoded("dtstart").astimezone(india).strftime("%H:%M")) for e in first_day] == [
        ("VbN", "09:00"), ("SOM", "10:45"), ("OR", "12:30"),
        ("MACR(S2)", "15:00"), ("VbN", "16:45"), ("VbN", "18:30"),
    ]
    exam = next(e for e in all_day if str(e["summary"]) == "END TERM EXAMINATION")
    assert exam.decoded("dtstart") == date(2026, 11, 30)
    assert exam.decoded("dtend") == date(2026, 12, 6)


def test_start_date_override_filters_classes_and_holidays(tmp_path):
    output = tmp_path / "exams.ics"
    assert main(["--start-date", "2026-11-30", "--output", str(output)]) == 0
    events = Calendar.from_ical(output.read_bytes()).walk("VEVENT")
    assert len(events) == 1
    assert str(events[0]["summary"]) == "END TERM EXAMINATION"
