"""
search WhatsOnStage.com for all Sondheim shows,
extract info for each and compile a weekly email report
"""

import os

from datetime import datetime
from typing import List, Tuple
from bs4 import BeautifulSoup, FeatureNotFound
import re
import requests

import config
from .wos_constants import SHOWS, HTML_TEMPLATE, HTML_SHOW_TEMPLATE
from .wos_constants import QUERY_URL_TEMPLATE
from config import Config
from mailjet_rest import Client


def extract_info_links(html_content: str, show_name: str) -> Tuple[List[str], str]:
    """
    Extracts 'More Info' links for a specific show from WhatsOnStage search results HTML.

    Args:
        html_content (str): The HTML content of the search results page.
        show_name (str): The name of the show to filter the results by.

    Returns:
        List[str]: A list of URLs for the 'More Info' buttons related to the specified show.
        str: log
    """
    log = ""
    soup = BeautifulSoup(html_content, "html.parser")
    search_results_container = soup.find("div", id="search-results-container")
    if not search_results_container:
        return [], "search results container not found"
    articles = search_results_container.find_all("article", class_="col-12")
    more_info_urls: List[str] = []
    for article in articles:
        type_link_tag = article.find("a", class_="text-body-tertiary")
        if not type_link_tag or type_link_tag.get_text(strip=True).upper() != "SHOW":
            continue
        article_title_tag = article.find("h3", class_="fw-bold").find("a")
        if not article_title_tag:
            continue
        article_title = article_title_tag.get_text(strip=True)
        if article_title.strip().lower() != show_name.strip().lower():
            log += f"skipping: {article_title}"
            continue
        more_info_links_in_article = article.find_all("a", class_="buy-tickets-link")
        for link in more_info_links_in_article:
            span_tag = link.find("span", string="More Info")
            if span_tag:
                href = link.get("href")
                if href:
                    more_info_urls.append(href)
                break
    if more_info_urls:
        log += f"found {len(more_info_urls)} show info links: {more_info_urls}"
    else:
        log += "no show info links"
    return more_info_urls, log


def extract_details_from_info_page(
    show_name: str, show_info_page_html: str
) -> Tuple[str, str]:
    """
    Formats and returns details for a show from its info page HTML.

    Args:
        show_name (str): The name of the show.
        show_info_page_html (str): The HTML content of the show's info page.

    Returns:
        Tuple[str, str]: A tuple containing the formatted string and the HTML snippet for the show.
    """
    soup = BeautifulSoup(show_info_page_html, "html.parser")
    opening_night = "N/A"
    closing_night = "N/A"
    first_preview = "N/A"
    venue_name = "N/A"
    venue_url = "N/A"
    info_url = "N/A"
    result = ""
    try:
        canonical_link = soup.find("link", rel="canonical")
        if canonical_link and canonical_link.get("href"):
            info_url = canonical_link["href"]
        else:
            og_url = soup.find("meta", property="og:url")
            if og_url and og_url.get("content"):
                info_url = og_url["content"]
    except FeatureNotFound as e:
        result += f"Feature not found: {e}"
    except Exception:
        pass
    try:
        dates_section = soup.find(class_="dates-section")
        if dates_section:
            first_preview_p_tag = dates_section.find(
                "p", string=re.compile("first preview", re.IGNORECASE)
            )
            if first_preview_p_tag:
                first_preview = first_preview_p_tag.text.strip().replace(
                    "First Preview", ""
                )
            opening_night_p_tag = dates_section.find(
                "p", string=re.compile("opening night", re.IGNORECASE)
            )
            if opening_night_p_tag:
                opening_night = opening_night_p_tag.text.strip().replace(
                    "Opening Night", ""
                )
            closing_night_p_tag = dates_section.find(
                "p", string=re.compile("closing night", re.IGNORECASE)
            )
            if closing_night_p_tag:
                closing_night = closing_night_p_tag.text.strip().replace(
                    "Closing Night", ""
                )
    except FeatureNotFound as e:
        result += f"Feature not found: {e}"
    except Exception:
        pass
    try:
        location_section = soup.find("div", class_="location-section")
        if location_section:
            block_detail_div = location_section.find("div", class_="block-detail")
            if block_detail_div:
                venue_link_tag = block_detail_div.find("a")
                if venue_link_tag:
                    venue_name = venue_link_tag.get_text(strip=True)
                    venue_url = venue_link_tag.get("href")
    except FeatureNotFound as e:
        result += f"Feature not found: {e}"
    except Exception:
        pass
    result += (
        f"show: {show_name}"
        + f" first preview: {first_preview} "
        + f" date: {opening_night} to {closing_night}"
        + f" venue: {venue_name} url: {venue_url} "
        + f" extracted from: {info_url}"
        + f" {os.linesep}"
        + f" {os.linesep}"
    )
    html_result = HTML_SHOW_TEMPLATE.format(
        show_name=show_name,
        first_preview=first_preview,
        opening_night=opening_night,
        closing_night=closing_night,
        venue_name=venue_name,
        venue_url=venue_url,
        info_url=info_url,
    )
    return result, html_result


def get_show_page(show_name: str) -> str:
    """
    Retrieves the HTML content of the search results page for a given show name from WhatsOnStage.

    Args:
        show_name (str): The name of the show to search for.

    Returns:
        str: The HTML content of the search results page.
    """
    query_url = QUERY_URL_TEMPLATE.format(show_name=show_name.replace(" ", "+"))

    try:
        response = requests.get(query_url, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        # Handle error appropriately
        return ""


def get_info_page(info_url: str) -> Tuple[str, str]:
    """
    Retrieves the HTML content of a show's info page from WhatsOnStage.

    Args:
        info_url (str): The URL of the show's info page.

    Returns:
        str: The HTML content of the info page.
        str: An error message if the request fails, otherwise an empty string.
    """

    try:
        response = requests.get(info_url, timeout=30)
        response.raise_for_status()
        return response.text, ""  # Return the HTML content and an empty error message
    except requests.RequestException as e:
        return "", f"Failed to fetch {info_url}: {e}"  # or raise based on requirements


def search_shows(shows: List[str]) -> Tuple[str, str]:
    """
    Searches for each show in the provided list, extracts info URLs, and compiles the information.

    Args:
        shows (List[str]): A list of show names to search for.

    Returns:
        str: A compiled string of extracted show information for all shows.
    """
    result = ""
    html_aggregate = ""
    for show_name in shows:
        result += (
            f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}]"
            f" searching show {show_name}..."
        )
        show_page_html = get_show_page(show_name)
        info_urls, log = extract_info_links(show_page_html, show_name)
        for info_url in info_urls:
            show_info_page_html, errors = get_info_page(info_url)
            if not errors:
                text_result, html_result = extract_details_from_info_page(
                    show_name, show_info_page_html
                )
            else:
                text_result = f"Error fetching info page for {show_name}: {errors}"
                html_result = (
                    f"<p>Error fetching info page for {show_name}: {errors}</p>"
                )
            result += text_result
            html_aggregate += html_result
    html_report = HTML_TEMPLATE.format(content=html_aggregate)
    result += log
    return result, html_report


def send_email(subject: str, html_body: str):
    #    def send_email_via_mailjet(api_key, secret_key, recipient_email, html_body):
    """
    Sends an email using Mailjet API

    Args:
        subject (str): sibject line
        html_body (str): HTML content for the email body

    Returns:
        tuple: (status_code, response_json)
    """

    config = Config().load_and_validate()
    mailjet = Client(
        auth=(config.mailjet_api_key, config.mailjet_secret), version="v3.1"
    )

    to_list = [{"Email": config.email_recipient, "Name": "Recipient"}]
    if getattr(config, "email_recipient_2", ""):
        to_list.append({"Email": config.email_recipient_2, "Name": "Recipient"})

    email_data = {
        "Messages": [
            {
                "From": {
                    "Email": config.email_sender,
                    "Name": "Sondheim Alert",
                },
                "To": to_list,
                "Subject": subject,
                "HTMLPart": html_body,
            }
        ]
    }

    response = mailjet.send.create(data=email_data)
    return response.status_code, response.json()


def handle(event, context):
    """
    Netlify serverless handler for Sondheim WhatsOnStage report.
    """
    result, html_report = search_shows(SHOWS)
    (status_code, response_json) = send_email(
        subject=f"Sondheim UK Report For {datetime.now().strftime('%B %d, %Y')}",
        html_body=html_report,
    )
    return {"statusCode": status_code, "body": response_json, "log": result}
