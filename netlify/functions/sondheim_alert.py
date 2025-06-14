import json
import sys
import os
from typing import Dict, Any

# Add the parent directory to the path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from config import config
from venue_finder import VenueFinder
from email_sender import EmailSender

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Netlify Functions handler for Sondheim Alert
    Can be triggered by scheduled functions or manual invocation
    """
    try:
        # Validate configuration
        config.validate()
        
        # Parse request body if present (for manual triggers)
        body = {}
        if event.get('body'):
            try:
                body = json.loads(event['body'])
            except json.JSONDecodeError:
                pass
        
        # Allow override of configuration via request body
        max_venues = body.get('max_venues', config.max_venues)
        user_location = body.get('user_location', config.user_location)
        search_radius = body.get('search_radius_miles', config.search_radius_miles)
        
        # Initialize services
        venue_finder = VenueFinder()
        email_sender = EmailSender(config.sendgrid_api_key, config.email_sender)
        
        # Search for venues
        print(f"Searching for Sondheim productions near {user_location}")
        
        # For now, using mock data - in production you'd use real search
        all_venues = venue_finder.get_mock_venues()
        
        # Filter by distance and limit results
        filtered_venues = venue_finder.filter_by_distance(
            all_venues, 
            user_location, 
            search_radius
        )
        
        # Limit to max venues
        top_venues = filtered_venues[:max_venues]
        
        print(f"Found {len(top_venues)} venues within {search_radius} miles")
        
        # Send email notification
        email_sent = email_sender.send_venue_alert(
            config.email_recipient,
            top_venues,
            user_location
        )
        
        # Prepare response
        response_data = {
            'success': True,
            'venues_found': len(top_venues),
            'email_sent': email_sent,
            'venues': top_venues,
            'search_location': user_location,
            'search_radius': search_radius
        }
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(response_data, indent=2)
        }
        
    except ValueError as e:
        # Configuration error
        print(f"Configuration error: {e}")
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'success': False,
                'error': 'Configuration error',
                'message': str(e)
            })
        }
        
    except Exception as e:
        # General error
        print(f"Unexpected error: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'success': False,
                'error': 'Internal server error',
                'message': str(e)
            })
        }

# For testing locally
if __name__ == "__main__":
    # Mock event for local testing
    test_event = {
        'httpMethod': 'POST',
        'body': json.dumps({
            'user_location': 'New York, NY',
            'max_venues': 3,
            'search_radius_miles': 100
        })
    }
    
    result = handler(test_event, None)
    print(json.dumps(result, indent=2))