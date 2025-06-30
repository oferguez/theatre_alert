from pprint import PrettyPrinter
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from netlify.functions.wos_sondheim_alert import send_email


def test_send_email():
    with open("tests/inttest/sample_report.html", "r", encoding="utf-8") as f:
        html_content_from_file = f.read()
    subject = f"TEST Sondheim UK Report For {datetime.now().strftime('%B %d, %Y')}"
    (status_code, response_json) = send_email(
        subject=subject, html_body=html_content_from_file
    )
    print(status_code)
    print(PrettyPrinter().pprint(response_json))


if __name__ == "__main__":
    test_send_email()
