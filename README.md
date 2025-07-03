# Theatre Alert

A serverless Python application that runs daily on Netlify to find Sondheim productions near you and send email notifications.

## Project Architecture

```
project_root/
├── netlify/
│   └── functions/
│       ├── wos_sondheim_alert.py   # Main logic: scraping, parsing, reporting, email
│       ├── wos_constants.py        # Show list, HTML templates, query templates
│       └── ...
├── obs/                            # Output HTML reports and logs
├── tests/
│   ├── inttests/                   # Integration tests (end-to-end, real HTML)
│   │   ├── test_wos_sondheim_alert.py
│   │   └── test_config.py          # Integration test for config
│   │   └── test_email_sender.py    # Integration test for email sending
│   └── unittests/                  # Unit tests (mocked HTML, no network)
│       └── test_wos_sondheim_alert.py
├── config.py                       # Configuration loading/validation (singleton pattern)
├── requirements.txt                # Python dependencies
├── README.md                       # This file
└── ...
```

- **netlify/functions/**: All Netlify serverless function code and scraping logic.
- **obs/**: Stores generated HTML reports and logs.
- **tests/inttests/**: Integration tests that run the full flow, using real or large HTML files, or test config loading and email sending.
- **tests/unittests/**: Unit tests for individual functions, using mocked HTML and monkeypatching network calls.
- **config.py**: Singleton config loader/validator, used everywhere as `from config import config`.

## How to Run Unit Tests

Unit tests are in `tests/unittests/` and use `pytest`:

```bash
# From project root, with venv activated
pytest tests/unittests/test_wos_sondheim_alert.py
```

- These tests use fixtures and monkeypatching to avoid real network calls.
- You can debug with VS Code using the provided launch configuration: "Debug Pytest Unit Tests".

## How to Run Integration Tests

Integration tests are in `tests/inttests/` and use real HTML files and the full scraping flow, or test config loading and email sending:

```bash
# From project root, with venv activated
python -m tests.inttests.test_wos_sondheim_alert
python -m tests.inttests.test_config
python -m tests.inttests.test_email_sender
```

- These tests may read from files in `obs/` and can exercise the full scraping, reporting, and email pipeline.
- You can also run other integration tests in this folder similarly.
- You can run the config integration test from VS Code using the task: "Integration Test: test_config.py".

## Manual Testing

Test the function locally:
```bash
python netlify/functions/theatre_alert.py
```

Test via HTTP (after deployment):
```bash
curl -X POST https://your-site.netlify.app/.netlify/functions/theatre_alert \
  -H "Content-Type: application/json" \
  -d '{"user_location": "London, UK", "max_venues": 5}'
```

## Configuration

All parameters are configurable via environment variables:

- `EMAIL_RECIPIENT`: Email address to receive notifications
- `EMAIL_RECIPIENT_2`: (Optional) Second recipient
- `EMAIL_SENDER`: Sender email address
- `MAILJET_API_KEY`: Mailjet API key for email sending
- `MAILJET_SECRET_KEY`: Mailjet secret key for email sending
- `GOOGLE_PLACES_API_KEY`: (Optional) For future venue search
- `SEARCH_RADIUS_MILES`: Search radius in miles (default: 50)

## Scheduling

The function runs daily at 9 AM UTC by default. Modify the schedule in `netlify.toml`:

```toml
[[functions]]
  schedule = "0 9 * * *"  # Daily at 9 AM UTC
  name = "theatre_alert"
```

## Email Format

The service sends HTML emails with:
- List of found productions
- Venue names and locations
- Performance dates
- Distance from your location
- Links to more information

## Development

- The main scraping, parsing, and email logic is in `netlify/functions/wos_sondheim_alert.py`.
- Configuration is loaded and validated via the singleton in `config.py`.
- Extend venue search by editing `venue_finder.py` (future use).
- Add new tests in `tests/unittests/` (unit) or `tests/inttests/` (integration).

## License

MIT License
