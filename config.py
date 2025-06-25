"""
Configuration module for Theatre Alert application.

This module handles environment variable loading and validation for the serverless
function that monitors theatre venues and sends email alerts.
"""

import os


class Config:  # pylint: disable=too-few-public-methods
    """
    Configuration class that loads and validates environment variables.

    This class centralizes all configuration management for the theatre alert
    system, including API keys, user preferences, and email settings.
    """

    def __init__(self) -> None:
        """Initialize configuration from environment variables."""
        self.email_recipient = os.getenv("EMAIL_RECIPIENT", "")
        self.email_sender = os.getenv("EMAIL_SENDER", "")
        self.mailjet_api_key = os.getenv("MAILJET_API_KEY", "")
        self.mailjet_secret = os.getenv("MAILJET_SECRET_KEY", "")
        # future use maybe sometime somewhere
        self.google_places_api_key = os.getenv("GOOGLE_PLACES_API_KEY", "")
        self.search_radius_miles = int(os.getenv("SEARCH_RADIUS_MILES", "50"))

    def validate(self) -> bool:
        """
        Validate that all required configuration values are present.

        Returns:
            bool: True if all required fields are present

        Raises:
            ValueError: If any required environment variable is missing
        """
        required_fields = [
            "email_recipient",
            "email_sender",
            "mailjet_api_key",
            "mailjet_secret",
        ]

        for field in required_fields:
            if not getattr(self, field):
                raise ValueError(
                    f"Missing required environment variable: {field.upper()}"
                )

        return True


config = Config()
