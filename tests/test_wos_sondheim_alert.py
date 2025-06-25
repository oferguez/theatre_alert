import os
import sys
import datetime

project_root = os.path.dirname(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
netlify_functions_path = os.path.join(project_root, 'netlify/functions')
if netlify_functions_path not in sys.path:
    sys.path.insert(0, netlify_functions_path)

from wos_sondheim_alert import extract_info_links, extract_details_from_info_page, search_shows
from wos_constants import SHOWS
import subprocess

def test_html_parser_show_page() -> None:
    """
    Reads a local HTML file, extracts 'More Info' links for the show "The Frogs",
    and prints the result.
    """
    with open("./obs/wos.html", "r", encoding="utf-8") as f:
        html_content_from_file = f.read()
        result = extract_info_links(html_content_from_file, "The Frogs")
        print(f"result: {result}")

def test_html_parser_show_info() -> None:
    """
    Reads a local HTML file, extracts details for the show "The Frogs",
    and prints the result.
    """
    with open("./obs/wos_info.html", "r", encoding="utf-8") as f:
        html_content_from_file = f.read()
        result = extract_details_from_info_page(
            "The Frogs", html_content_from_file
        )
        print(result)

def test_flow() -> None:
    """
    Full flow: runs the main search and prints/saves the HTML report.
    """
    result, html_report = search_shows(SHOWS)
    filename = f"./obs/{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_report.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_report)
    print("-" * 30)
    print(result)
    print("-" * 30)
    print(f"HTML report saved to {filename}")
    if "WSL_DISTRO_NAME" in os.environ:
        completed = subprocess.run(["wslpath", "-w", filename], capture_output=True, text=True)
        windows_path = completed.stdout.strip()
        subprocess.run(["explorer.exe", windows_path])


if __name__ == "__main__":
    test_flow()
