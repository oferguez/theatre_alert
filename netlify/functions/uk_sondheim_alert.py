"""
Netlify Event Handler for UK Sondheim Theatre Alerts

This module is designed to be run as a Netlify serverless function. It fetches, processes, and 
formats Sondheim-related theatre event data in the UK, returning a formatted summary suitable for 
email or alert delivery. The workflow is as follows:

handler(event, context)
    Input:  event (dict), context (object)
    Output: dict with 'statusCode' and 'body' (str)
    - Main entry point for Netlify. Fetches calendar data, extracts events, categorizes and sorts 
      them, and formats the result for output.

fetch_calendar_data()
    Input:  None
    Output: str (raw response text from the calendar API)
    - Sends a POST request to the Sondheim Society events calendar API and returns the raw response.

extract_events(raw_text)
    Input:  raw_text (str)
    Output: list of event dicts
    - Extracts and parses the list of event items from the raw calendar data text.

categorize_and_sort(events, current_date)
    Input:  events (list of dict), current_date (datetime)
    Output: tuple (current, upcoming), each a list of event dicts
    - Categorizes events into current and upcoming, sorts current by distance from London, and 
      upcoming by start date.

format_email(current, upcoming)
    Input:  current (list of dict), upcoming (list of dict)
    Output: str (formatted summary)
    - Formats the current and upcoming events into a human-readable summary for email or alerts.
"""

from datetime import datetime
import json
import re
from geopy.distance import geodesic
import requests

# CONFIG: Reference point for distance sorting (London) TODO take from cfg
CONFIG_LOCATION = (51.53166, -0.09592)

def fetch_calendar_data():
    """
    Fetches calendar data from the Sondheim Society events calendar API.

    Sends a POST request to the specified calendar data endpoint with 
    required headers and form data, emulating a browser request from the 
    Sondheim Society website. Raises an exception if the request fails.

    Returns:
        str: The raw response text containing the calendar data.

    Raises:
        Exception: If the HTTP request to fetch the calendar data is unsuccessful.
    """
    url = 'https://inffuse.eventscalendar.co/js/v0.1/calendar/data'
    headers = {
        'accept': '*/*',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://plugin.eventscalendar.co',
        'referer': (
            'https://plugin.eventscalendar.co/widget.html?pageId=hh2t2&compId=comp-m7kbpz0j'
        ),
        'user-agent': 'Mozilla/5.0'
    }
    data = {
        '_referrer': 'https://www.sondheimsociety.com/',
        '_origin': (
            'https://plugin.eventscalendar.co/widget.html?pageId=hh2t2&compId=comp-m7kbpz0j'
        ),
        'app': 'calendar'
    }

    response = requests.post(url, headers=headers, data=data, timeout=15)
    if not response.ok:
        response.raise_for_status()  # pylint: disable=broad-except
    return response.text

def extract_events(raw_text):
    """
    Extracts a list of events from a raw JSON-like text string.

    The function searches for a JSON array associated with the "items" key in the input text,
    parses it, and returns the resulting list of events. If the pattern is not found, it returns
    an empty list.

    Args:
        raw_text (str): The raw text containing the JSON data.

    Returns:
        list: A list of events extracted from the "items" array, or an empty list if not found.
    """
    match = re.search(r'"items":(\[.*?\])\s*,\s*"total"', raw_text, re.DOTALL)
    if not match:
        return []
    return json.loads(match.group(1))

def categorize_and_sort(events, current_date):
    """
    Categorizes a list of event dictionaries into current and upcoming events based on the current
    date, and sorts them accordingly.

    Args:
        events (list): A list of event dictionaries, each containing at least 'title', 'start',
            'end', and optionally 'location' with 'venue' and 'coordinates'.
        current_date (datetime): The current date and time used to determine event status.

    Returns:
        tuple: A tuple (current, upcoming) where:
            - current (list): List of event dicts currently ongoing, sorted by distance from
              CONFIG_LOCATION (nearest first).
            - upcoming (list): List of event dicts that are upcoming, sorted by start date (soonest
              first).

    Notes:
        - Events with missing or malformed data are skipped.
        - Each event dict in the output contains: 'title', 'venue', 'start', 'end', and 'latlon'
          (tuple of latitude and longitude).
        - Events with missing coordinates are sorted last in the 'current' list.
    """
    current, upcoming = [], []
    for e in events:
        try:
            start = datetime.fromisoformat(e['start'].replace('Z', '+00:00'))
            end = datetime.fromisoformat(e['end'].replace('Z', '+00:00'))
            venue = e.get('location', {}).get('venue', 'Unknown Venue')
            coords = e.get('location', {}).get('coordinates', [None, None])
            lat, lon = coords if coords and len(coords) == 2 else (None, None)
            item = {
                "title": e['title'],
                "venue": venue,
                "start": start,
                "end": end,
                "latlon": (lat, lon)
            }
            if start <= current_date <= end:
                current.append(item)
            elif start > current_date:
                upcoming.append(item)
        except:  # pylint: disable=bare-except
            continue

    def distance(item):
        if None in item['latlon']:
            return float('inf')
        return geodesic(CONFIG_LOCATION, item['latlon']).kilometers

    current.sort(key=distance)
    upcoming.sort(key=lambda e: e['start'])
    return current, upcoming

def format_email(current, upcoming):
    """
    Formats information about current and upcoming Sondheim productions in the UK into a human-
    readable email body.

    Args:
        current (list of dict): A list of dictionaries representing current productions. Each
            dictionary should have keys 'title', 'venue', 'start', and 'end', where 'start' and
            'end' are datetime objects.
        upcoming (list of dict): A list of dictionaries representing upcoming productions. Each
            dictionary should have keys 'title', 'venue', 'start', and 'end', where 'start' and
            'end' are datetime objects.

    Returns:
        str: A formatted string suitable for use as an email body, listing current and upcoming
            Sondheim productions.
    """
    def fmt(e):
        date_range = f"{e['start'].date()} to {e['end'].date()}"
        return f"- {e['title']} @ {e['venue']} ({date_range})"

    body = ["🎭 *Current Sondheim Productions in the UK:*"]
    body += [fmt(e) for e in current] if current else ["(None currently running.)"]

    body += ["\n📅 *Upcoming Sondheim Productions:*"]
    body += [fmt(e) for e in upcoming] if upcoming else ["(None announced.)"]
    return '\n'.join(body)

def handler(_event, _context):
    """
    Handles incoming event and context, processes calendar data, returns formatted email content.

    Args:
        event (dict): The event data passed to the handler, typically containing request info.
        context (object): The context in which the handler is called, providing runtime information.

    Returns:
        dict: A dictionary with 'statusCode' and 'body' keys. On success, 'statusCode' is 200 and
            'body' contains the formatted email content. On failure, 'statusCode' is 500 and 'body'
            contains the error message.
    """
    try:
        raw_data = fetch_calendar_data()
        events = extract_events(raw_data)
        current, upcoming = categorize_and_sort(events, datetime.utcnow())
        result = format_email(current, upcoming)
        return {
            "statusCode": 200,
            "body": result
        }
    except Exception as e:  # pylint: disable=broad-except
        return {
            "statusCode": 500,
            "body": f"Error: {str(e)}"
        }

def main():
    response = handler({}, {})
    print(f"Status: {response['statusCode']}\n")
    print(response['body'])

if __name__ == "__main__":
    main()