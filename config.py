import os
from typing import Dict, Any

class Config:
    def __init__(self):
        self.max_venues = int(os.getenv('MAX_VENUES', '3'))
        self.user_location = os.getenv('USER_LOCATION', 'New York, NY')
        self.search_radius_miles = int(os.getenv('SEARCH_RADIUS_MILES', '50'))
        self.email_recipient = os.getenv('EMAIL_RECIPIENT', '')
        self.email_sender = os.getenv('EMAIL_SENDER', '')
        self.sendgrid_api_key = os.getenv('SENDGRID_API_KEY', '')
        self.google_places_api_key = os.getenv('GOOGLE_PLACES_API_KEY', '')
        
    def validate(self) -> bool:
        required_fields = [
            'email_recipient',
            'email_sender', 
            'sendgrid_api_key'
        ]
        
        for field in required_fields:
            if not getattr(self, field):
                raise ValueError(f"Missing required environment variable: {field.upper()}")
        
        return True

config = Config()