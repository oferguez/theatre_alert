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

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def _load(self) -> None:
        """Initialize configuration from environment variables."""
        self.email_recipient = os.getenv("EMAIL_RECIPIENT", "")
        self.email_recipient_2 = os.getenv("EMAIL_RECIPIENT_2", "")
        self.email_sender = os.getenv("EMAIL_SENDER", "")
        self.mailjet_api_key = os.getenv("MAILJET_API_KEY", "")
        self.mailjet_secret = os.getenv("MAILJET_SECRET_KEY", "")
        # future use maybe sometime somewhere
        self.google_places_api_key = os.getenv("GOOGLE_PLACES_API_KEY", "")
        self.search_radius_miles = int(os.getenv("SEARCH_RADIUS_MILES", "50"))

    def _validate(self) -> bool:
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

    def load_and_validate(self) -> "Config":
        """
        Load environment variables and validate required fields.

        Raises:
            ValueError: If any required environment variable is missing
        """
        self._load()
        if not self._validate():
            raise ValueError("Configuration validation failed")
        return self
