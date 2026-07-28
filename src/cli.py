from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import Sequence
from zoneinfo import ZoneInfoNotFoundError

from pypdf.errors import PdfReadError

from src.calendar_builder import build_calendar
from src.config import CALENDAR_NAME, INPUT_FILENAME, LOCATION, OUTPUT_FILENAME, REMINDER_MINUTES, TIMEZONE
from src.parser import parse_pdf_schedule
from src.validator import CalendarValidationError, ValidationReport, validate_calendar_file


LOGGER = logging.getLogger(__name__)
EXIT_SUCCESS = 0
EXIT_ERROR = 1


class CalendarGenerationError(Exception):
    """Raised when calendar generation cannot continue."""


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command-line calendar generation flow."""
    configure_logging()
    args = parse_args(argv)

    try:
        if args.validate:
            report = validate_calendar_file(args.output)
            log_validation_report(report)
            return EXIT_SUCCESS if report.passed else EXIT_ERROR

        generate_calendar(args)
    except CalendarGenerationError as error:
        LOGGER.error("%s", error)
        return EXIT_ERROR
    except CalendarValidationError as error:
        LOGGER.error("%s", error)
        return EXIT_ERROR
    except PdfReadError:
        LOGGER.error("Invalid PDF: unable to read %s", args.input)
        return EXIT_ERROR
    except PermissionError as error:
        LOGGER.error("Permission denied: %s", error)
        return EXIT_ERROR
    except OSError as error:
        LOGGER.error("Invalid output path: %s", error)
        return EXIT_ERROR
    except ZoneInfoNotFoundError:
        LOGGER.error("Invalid timezone: %s", args.timezone)
        return EXIT_ERROR

    return EXIT_SUCCESS


def configure_logging() -> None:
    """Configure console logging for CLI output."""
    logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stdout)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments for calendar generation."""
    parser = argparse.ArgumentParser(description="Generate an ICS calendar from an IIM schedule PDF.")
    parser.add_argument(
        "pdf",
        nargs="?",
        type=Path,
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--input",
        dest="input",
        default=None,
        type=Path,
        help=f"Path to the schedule PDF. Default: {INPUT_FILENAME}",
    )
    parser.add_argument(
        "--output",
        default=OUTPUT_FILENAME,
        type=Path,
        help=f"Path for the generated ICS file. Default: {OUTPUT_FILENAME}",
    )
    parser.add_argument(
        "--calendar-name",
        default=CALENDAR_NAME,
        help=f"Calendar name. Default: {CALENDAR_NAME}",
    )
    parser.add_argument(
        "--location",
        default=LOCATION,
        help="Location to add to each event.",
    )
    parser.add_argument(
        "--timezone",
        default=TIMEZONE,
        help="Timezone for generated event timestamps, such as Asia/Kolkata.",
    )
    parser.add_argument(
        "--reminder",
        default=REMINDER_MINUTES,
        type=int,
        help="Reminder minutes before each event.",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help=f"Validate the generated calendar file. Default: {OUTPUT_FILENAME}",
    )

    args = parser.parse_args(argv)
    args.input = args.input or args.pdf or INPUT_FILENAME
    return args


def generate_calendar(args: argparse.Namespace) -> None:
    """Generate a calendar using parsed CLI arguments."""
    log_header()
    validate_input_path(args.input)
    validate_output_path(args.output)

    LOGGER.info("Reading PDF...")
    LOGGER.info("")
    LOGGER.info("Parsing timetable...")
    schedule_items = parse_pdf_schedule(args.input)
    if not schedule_items:
        raise CalendarGenerationError("Unable to parse timetable: no classes found in the PDF.")

    LOGGER.info("")
    LOGGER.info("Found %s classes", len(schedule_items))
    LOGGER.info("")
    LOGGER.info("Generating calendar...")
    calendar = build_calendar(
        schedule_items,
        calendar_name=args.calendar_name,
        location=args.location,
        timezone=args.timezone,
        reminder_minutes=args.reminder,
    )

    LOGGER.info("")
    LOGGER.info("Saving output...")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(calendar.to_ical())

    LOGGER.info("")
    LOGGER.info("Done.")
    LOGGER.info("")
    LOGGER.info("Output:")
    LOGGER.info("%s", args.output)


def log_header() -> None:
    """Log the application header."""
    LOGGER.info("----------------------------------------")
    LOGGER.info("IIM Calendar Generator")
    LOGGER.info("----------------------------------------")
    LOGGER.info("")


def log_validation_report(report: ValidationReport) -> None:
    """Log a validation report for an existing calendar."""
    LOGGER.info("----------------------------------------")
    LOGGER.info("Calendar Validation")
    LOGGER.info("----------------------------------------")
    LOGGER.info("")
    LOGGER.info("Events: %s", report.event_count)
    LOGGER.info("")
    LOGGER.info("Duplicate Events: %s", report.duplicate_events)
    LOGGER.info("")
    LOGGER.info("Invalid Dates: %s", report.invalid_dates)
    LOGGER.info("")
    LOGGER.info("Invalid Time Ranges: %s", report.invalid_time_ranges)
    LOGGER.info("")
    LOGGER.info("Missing Summary: %s", report.missing_summary)
    LOGGER.info("")
    LOGGER.info("Missing DTSTART: %s", report.missing_dtstart)
    LOGGER.info("")
    LOGGER.info("Missing DTEND: %s", report.missing_dtend)
    LOGGER.info("")
    LOGGER.info("Missing Location: %s", report.missing_location)
    LOGGER.info("")
    LOGGER.info("Missing Reminder: %s", report.missing_valarm)
    LOGGER.info("")
    LOGGER.info("Validation %s", "Passed" if report.passed else "Failed")


def validate_input_path(input_path: Path) -> None:
    """Validate the input PDF path before parsing."""
    if not input_path.exists():
        raise CalendarGenerationError(f"Missing PDF: {input_path}")

    if not input_path.is_file():
        raise CalendarGenerationError(f"Missing PDF: {input_path} is not a file")


def validate_output_path(output_path: Path) -> None:
    """Validate the output ICS path before writing."""
    if output_path.exists() and output_path.is_dir():
        raise CalendarGenerationError(f"Invalid output path: {output_path} is a directory")

    if not output_path.name:
        raise CalendarGenerationError(f"Invalid output path: {output_path}")
