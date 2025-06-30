# Theatre Alert

A serverless Python application that runs daily on Netlify to find Sondheim productions near you and send email notifications.

## Project Architecture

```
project_root/
├── netlify/
│   └── functions/
│       ├── wos_sondheim_alert.py   # Main logic: scraping, parsing, reporting
│       ├── wos_constants.py        # Show list, HTML templates, query templates
│       └── ...
├── obs/                            # Output HTML reports and logs
├── tests/
│   ├── inttest/                    # Integration tests (end-to-end, real HTML)
│   │   └── test_wos_sondheim_alert.py
│   └── unittests/                  # Unit tests (mocked HTML, no network)
│       └── test_wos_sondheim_alert.py
├── config.py                       # Configuration loading/validation
├── requirements.txt                # Python dependencies
├── README.md                       # This file
└── ...
```

- **netlify/functions/**: All Netlify serverless function code and scraping logic.
- **obs/**: Stores generated HTML reports and logs.
- **tests/inttest/**: Integration tests that run the full flow, using real or large HTML files.
- **tests/unittests/**: Unit tests for individual functions, using mocked HTML and monkeypatching network calls.

## How to Run Unit Tests

Unit tests are in `tests/unittests/` and use `pytest`:

```bash
# From project root, with venv activated
pytest tests/unittests/test_wos_sondheim_alert.py
```

- These tests use fixtures and monkeypatching to avoid real network calls.
- You can debug with VS Code using the provided launch configuration: "Debug Pytest Unit Tests".

## How to Run Integration Tests

Integration tests are in `tests/inttests/` and use real HTML files and the full scraping flow:

```bash
# From project root, with venv activated
python -m tests.inttests.test_wos_sondheim_alert
```

- These tests may read from files in `obs/` and can exercise the full scraping and reporting pipeline.
- You can also run other integration tests in this folder similarly.

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

- `MAX_VENUES`: Maximum number of venues to return
- `USER_LOCATION`: Your location for proximity search
- `SEARCH_RADIUS_MILES`: Search radius in miles
- `EMAIL_RECIPIENT`: Email address to receive notifications
- `EMAIL_SENDER`: Sender email address
- `SENDGRID_API_KEY`: SendGrid API key for email sending

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

To extend the venue search functionality:
1. Implement real web scraping in `venue_finder.py`
2. Add new theater websites to search
3. Enhance the email template in `email_sender.py`

## License

MIT License
