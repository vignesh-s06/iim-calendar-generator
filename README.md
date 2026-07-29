# IIM Calendar Generator

Generate an `.ics` calendar file from an IIM timetable PDF.

## Project Structure

```text
iim-calendar-generator/
|-- .github/
|   `-- workflows/
|       |-- ci.yml
|       `-- deploy-pages.yml
|-- input/
|   `-- schedule.pdf
|-- output/
|   |-- .gitkeep
|   `-- iim-calendar.ics
|-- src/
|   |-- parser.py
|   |-- calendar_builder.py
|   |-- cli.py
|   |-- config.py
|   |-- utils.py
|   `-- validator.py
|-- tests/
|-- generate_calendar.py
|-- requirements.txt
|-- README.md
|-- .gitignore
`-- LICENSE
```

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
python generate_calendar.py
```

By default, the script reads:

```text
input/schedule.pdf
```

and writes:

```text
output/iim-calendar.ics
```

You can also provide custom paths:

```bash
python generate_calendar.py --input input/schedule.pdf --output output/custom-calendar.ics
```

CLI options:

```text
--input          Path to the schedule PDF
--output         Path for the generated ICS file
--calendar-name  Calendar name shown in calendar apps
--location       Location added to each event
--timezone       Timezone, such as Asia/Kolkata
--reminder       Reminder minutes before each event
--validate       Validate the generated calendar file without modifying it
```

Examples:

```bash
python generate_calendar.py --calendar-name "PGPEx Term III"
```

```bash
python generate_calendar.py --location "NAB G08" --timezone Asia/Kolkata --reminder 15
```

```bash
python generate_calendar.py --input input/schedule.pdf --output output/iim-calendar.ics
```

Validate the generated calendar:

```bash
python generate_calendar.py --validate
```

Validate a custom output file:

```bash
python generate_calendar.py --validate --output output/custom-calendar.ics
```

## Reminder Subjects

Reminders are attached only for subjects listed in `REMINDER_SUBJECTS` in `src/config.py`.

To change which subjects receive reminders, edit:

```python
REMINDER_SUBJECTS = frozenset(
    {
        "CFFM",
        "CS(S2)",
        "DMV",
        "GTBL(S2)",
        "MHCGH",
    }
)
```

All subjects still generate calendar events. Subjects not listed in `REMINDER_SUBJECTS` are generated without `VALARM` reminders.

## Testing

Install the project requirements, then run:

```bash
pytest
```

The test suite includes unit tests for the parser, calendar builder, and utilities, plus an integration test that generates `output/iim-calendar.ics` from `input/schedule.pdf`.

## GitHub Pages Deployment

This project uses GitHub Pages as the only hosting solution. No server, VPS, database, or external cloud service is required.

Expected URLs after GitHub Pages is enabled:

```text
GitHub Pages URL: https://vignesh-s06.github.io/iim-calendar-generator/
Direct .ics URL: https://vignesh-s06.github.io/iim-calendar-generator/iim-calendar.ics
webcal URL: webcal://vignesh-s06.github.io/iim-calendar-generator/iim-calendar.ics
```

### GitHub Pages Setup

In the GitHub repository:

1. Go to `Settings` -> `Pages`.
2. Under `Build and deployment`, set `Source` to `GitHub Actions`.
3. Go to `Settings` -> `Actions` -> `General`.
4. Under `Workflow permissions`, allow workflows to read repository contents and write Pages deployments.
5. Push to the `main` branch or manually run `Deploy Calendar to GitHub Pages` from the Actions tab.

### How Deployment Works

On every push to `main`, `.github/workflows/deploy-pages.yml`:

1. Installs Python 3.13.
2. Installs dependencies from `requirements.txt`.
3. Runs `pytest`.
4. Generates `output/iim-calendar.ics`.
5. Copies the generated file into a Pages artifact.
6. Adds `.nojekyll`.
7. Deploys the artifact to GitHub Pages.

The deployed site contains the generated `iim-calendar.ics` file at the repository Pages URL.

### MIME Type Notes

GitHub Pages is static hosting and does not support custom server configuration such as `.htaccess` or manually assigned response headers. GitHub Pages generally serves files by extension, but this repository cannot force the `text/calendar` MIME type.

Most calendar apps can subscribe to a public `.ics` URL even when the server controls the MIME type. If a client refuses the URL or does not refresh reliably, the limitation is usually static hosting behavior or the calendar client's cache policy.

For the most reliable GitHub-based approach, use the direct GitHub Pages `.ics` URL or the `webcal://` URL and keep the filename stable. The workflow regenerates and redeploys the same `iim-calendar.ics` path on every push to `main`.

### Apple Calendar Subscription

Use this subscription URL:

```text
webcal://vignesh-s06.github.io/iim-calendar-generator/iim-calendar.ics
```

On iPhone:

1. Open `Settings`.
2. Tap `Calendar`.
3. Tap `Accounts`.
4. Tap `Add Account`.
5. Tap `Other`.
6. Tap `Add Subscribed Calendar`.
7. Enter `webcal://vignesh-s06.github.io/iim-calendar-generator/iim-calendar.ics`.
8. Tap `Next`.
9. Keep SSL enabled if shown.
10. Tap `Save`.

Apple Calendar controls refresh timing for subscribed calendars. Updates may not appear immediately after GitHub Pages republishes the file.

### Google Calendar Subscription

In Google Calendar on desktop:

1. Open Google Calendar.
2. Next to `Other calendars`, click `+`.
3. Choose `From URL`.
4. Enter `https://vignesh-s06.github.io/iim-calendar-generator/iim-calendar.ics`.
5. Click `Add calendar`.

Google Calendar controls refresh timing and may cache subscribed calendars for several hours.

### Updating the Timetable

To publish a new timetable:

1. Replace `input/schedule.pdf` with the latest PDF.
2. Run `python generate_calendar.py` locally if you want to preview the output.
3. Run `python generate_calendar.py --validate` locally if you want to validate the generated file.
4. Commit and push the updated PDF to the `main` branch.
5. GitHub Actions regenerates and republishes `iim-calendar.ics` automatically.
