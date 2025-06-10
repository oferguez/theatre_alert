# Sondheim Alert

A serverless Python application that runs daily on Netlify to find Stephen Sondheim productions near you and send email notifications.

## Features

- 🎭 Searches for current Stephen Sondheim productions
- 📍 Finds venues within a configurable radius of your location
- 📧 Sends email notifications with venue details
- ⚙️ Fully configurable via environment variables
- 🕐 Runs automatically daily or can be triggered manually
- 🚀 Deploys easily to Netlify Functions

## Setup

1. **Clone and install dependencies:**
   ```bash
   git clone <your-repo>
   cd sondheim_alert
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   Copy `.env.example` to `.env` and fill in your values:
   ```bash
   cp .env.example .env
   ```

   Required variables:
   - `EMAIL_RECIPIENT`: Your email address
   - `EMAIL_SENDER`: Sender email address  
   - `SENDGRID_API_KEY`: Your SendGrid API key

   Optional variables:
   - `MAX_VENUES`: Number of venues to find (default: 3)
   - `USER_LOCATION`: Your location (default: New York, NY)
   - `SEARCH_RADIUS_MILES`: Search radius in miles (default: 50)

3. **Deploy to Netlify:**
   - Connect your repository to Netlify
   - Set environment variables in Netlify dashboard
   - Deploy - the function will run daily automatically

## Manual Testing

Test the function locally:
```bash
python netlify/functions/sondheim_alert.py
```

Test via HTTP (after deployment):
```bash
curl -X POST https://your-site.netlify.app/.netlify/functions/sondheim_alert \
  -H "Content-Type: application/json" \
  -d '{"user_location": "Los Angeles, CA", "max_venues": 5}'
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
  name = "sondheim_alert"
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