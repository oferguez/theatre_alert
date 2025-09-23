"""
Unit test for culture officer that uses saved GPT results instead of calling the API.
"""

import os
import unittest
import logging
import ast
from unittest.mock import patch, MagicMock
from format_culture_html import parse_and_format_culture_html

# Force logging configuration for tests
logging.getLogger().handlers.clear()
logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s", force=True
)
logger = logging.getLogger("culture_officer")


class TestCultureOfficerFormatter(unittest.TestCase):
    """Test the culture officer formatter with saved GPT results."""

    def setUp(self):
        """Set up test fixtures."""
        self.debug_file_path = os.path.join(
            os.path.dirname(__file__), "culture_officer_debug.txt"
        )

    def test_parse_and_format_saved_gpt_results(self):
        """Test parsing and formatting of saved GPT results."""
        # Load saved GPT results from debug file
        with open(self.debug_file_path, "r", encoding="utf-8") as f:
            gpt_result_str = f.read()

        # Parse the string as a Python literal (dict)
        gpt_result = ast.literal_eval(gpt_result_str)

        # Format the results to HTML
        html_output = parse_and_format_culture_html(
            gpt_result["events"], gpt_result["bonus"]
        )

        # Verify HTML structure
        self.assertIn("<!doctype html>", html_output)
        self.assertIn("<html>", html_output)
        self.assertIn("Culture Officer Report", html_output)

        # Check for specific events from the saved results
        self.assertIn("Cow", html_output)
        self.assertIn("Royal Court Theatre", html_output)
        self.assertIn("Radical Harmony", html_output)
        self.assertIn("National Gallery", html_output)

        # Verify links are properly formatted
        self.assertIn("<a href=", html_output)

        # Check for bonus content
        self.assertIn("Bonus", html_output)
        self.assertIn("midnight screening", html_output)

    @patch("culture_officer.call_gpt_formatted_search_enabled")
    @patch("culture_officer.send_email")
    def test_handler_with_mock_gpt_response(self, mock_send_email, mock_call_gpt):
        """Test the handler function using saved GPT results instead of API call."""
        from culture_officer import handler
        from config import Config

        # Load saved GPT results
        with open(self.debug_file_path, "r", encoding="utf-8") as f:
            saved_gpt_result_str = f.read()

        # Parse the string as a Python literal (dict)
        saved_gpt_result = ast.literal_eval(saved_gpt_result_str)

        # Mock the GPT call to return saved results
        mock_call_gpt.return_value = saved_gpt_result

        # Mock email sending
        mock_send_email.return_value = (200, {"success": True})

        # Mock config
        with patch.object(Config, "load_and_validate") as mock_config:
            mock_config.return_value = MagicMock(debug=False)

            # Call the handler
            result = handler(None)

            # Verify the handler completed successfully
            self.assertEqual(result["statusCode"], 200)
            self.assertIn("success", str(result["body"]))

            # Verify the log contains HTML (which is now the formatted output)
            self.assertIn("<!doctype html>", result["log"])
            self.assertIn("Culture Officer Report", result["log"])

            # Verify GPT was "called" once
            mock_call_gpt.assert_called_once()

            # Verify email was sent once
            mock_send_email.assert_called_once()

    def test_html_output_file_creation(self):
        """Test that HTML file is created correctly from saved GPT results."""
        # Load saved GPT results
        with open(self.debug_file_path, "r", encoding="utf-8") as f:
            gpt_result_str = f.read()

        # Parse the string as a Python literal (dict)
        gpt_result = ast.literal_eval(gpt_result_str)

        # Format to HTML
        html_output = parse_and_format_culture_html(
            gpt_result["events"], gpt_result["bonus"]
        )

        # Save to test HTML file
        test_html_path = os.path.join(
            os.path.dirname(__file__), "test_culture_output.html"
        )
        with open(test_html_path, "w", encoding="utf-8") as f:
            f.write(html_output)

        # Verify file was created and has content
        self.assertTrue(os.path.exists(test_html_path))

        with open(test_html_path, "r", encoding="utf-8") as f:
            file_content = f.read()

        self.assertEqual(file_content, html_output)
        self.assertGreater(len(file_content), 1000)  # Should be substantial HTML

        # Clean up test file
        # os.remove(test_html_path)


if __name__ == "__main__":
    unittest.main()
