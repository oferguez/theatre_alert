import os
import sys
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

project_root = os.path.dirname(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
netlify_functions_path = os.path.join(project_root, "netlify/functions")
if netlify_functions_path not in sys.path:
    sys.path.insert(0, netlify_functions_path)

from wos_sondheim_alert import send_email


def test_send_email():
    with open("sample_report.html", "r", encoding="utf-8") as f:
        html_content_from_file = f.read()
    subject = f"Sondheim UK Report For {datetime.now().strftime('%B %d, %Y')}"
    send_email(subject=subject, html_body=html_content_from_file)


if __name__ == "__main__":
    test_send_email()
