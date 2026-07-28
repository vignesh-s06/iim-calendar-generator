from __future__ import annotations

from pathlib import Path

from src.cli import EXIT_ERROR, parse_args, main
from src.config import CALENDAR_NAME, INPUT_FILENAME, LOCATION, OUTPUT_FILENAME, REMINDER_MINUTES, TIMEZONE


def test_parse_args_uses_config_defaults() -> None:
    """Use config defaults when CLI options are omitted."""
    args = parse_args([])

    assert args.input == INPUT_FILENAME
    assert args.output == OUTPUT_FILENAME
    assert args.calendar_name == CALENDAR_NAME
    assert args.location == LOCATION
    assert args.timezone == TIMEZONE
    assert args.reminder == REMINDER_MINUTES


def test_parse_args_supports_cli_overrides() -> None:
    """Parse supported user-facing CLI options."""
    args = parse_args(
        [
            "--input",
            "custom/input.pdf",
            "--output",
            "custom/output.ics",
            "--calendar-name",
            "Custom Calendar",
            "--location",
            "NAB G08",
            "--timezone",
            "Asia/Kolkata",
            "--reminder",
            "15",
        ]
    )

    assert args.input == Path("custom/input.pdf")
    assert args.output == Path("custom/output.ics")
    assert args.calendar_name == "Custom Calendar"
    assert args.location == "NAB G08"
    assert args.timezone == "Asia/Kolkata"
    assert args.reminder == 15


def test_parse_args_supports_validation_mode() -> None:
    """Parse the calendar validation flag."""
    args = parse_args(["--validate"])

    assert args.validate is True


def test_main_returns_non_zero_for_missing_pdf() -> None:
    """Return an error exit code when the input PDF is missing."""
    exit_code = main(["--input", "missing.pdf"])

    assert exit_code == EXIT_ERROR
