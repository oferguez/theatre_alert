"""
    List[str]: A list of URLs for the 'More Info' buttons related to the specified show.
    ...

    Extracts and formats details from a show's info page HTML.

    show_name (str): The name of the show.
    show_info_page_html (str): The HTML content of the show's info page.

    str: A formatted string containing the show name and info page details.
    ...


    show_name (str): The name of the show to search for.

    str: The HTML content of the search results page.
    ...


    info_url (str): The URL of the show's info page.

    str: The HTML content of the info page.
    ...


    shows (List[str]): A list of show names to search for.

    str: A compiled string of extracted show information.
    ...


    Reads a local HTML file, extracts 'More Info' links for the show "The Frogs",
    and prints the result.
    ...

This script searches WhatsOnStage.com for a predefined list of Sondheim shows,
extracts relevant information for each show, and compiles a weekly email report.
It includes functions to parse HTML content, extract show information, and
retrieve web pages for each show.

Functions:
    extract_info_links(html_content: str, show_name: str) -> List[str]:
        Extracts 'More Info' links for a specific show from WhatsOnStage search results HTML.

    extract_show_info(info_url: str) -> str:
        Extracts and returns information for a show from its info URL.

    get_show_page(show_name: str) -> str:
        Retrieves the HTML content of the search results page for a given show name.

    get_info_page(info_url: str) -> str:
        Retrieves the HTML content of the info page for a given show.

    search_shows(shows: List[str]) -> str:
        Searches for each show in the provided list, extracts info URLs, and compiles
        the information into a single string.

    test_html_parser1():
        Test function to parse a local HTML file and print extracted info links for a specific show.
search WhatsOnStage.com for all Sondheim shows,
extract info for each and compile a weekly email report
"""

# pylint: disable=broad-except

import datetime
import os
import re
from typing import List, Optional, Tuple
import requests
from bs4 import BeautifulSoup, Tag

SHOWS_: List[str] = ["Company"]

SHOWS: List[str] = [
    "Saturday Night",
    "Candide",
    "West Side Story",
    "Gypsy",
    "A Funny Thing Happened on the Way to the Forum",
    "Anyone Can Whistle",
    "Do I Hear a Waltz?",
    "The Mad Show",
    "Evening Primrose",
    "Company",
    "Follies",
    "A Little Night Music",
    "The Frogs",
    "Pacific Overtures",
    "Side by Side by Sondheim",
    "Sweeney Todd",
    "Marry Me a Little",
    "Merrily We Roll Along",
    "Sunday in the Park with George",
    "Into the Woods",
    "Assassins",
    "Putting It Together",
    "Passion",
    "Road Show",
    "Here We Are",
    "Hot Spot",
]


def extract_info_links(html_content: str, show_name: str) -> List[str]:
    """
    Extracts 'More Info' links for a specific show from WhatsOnStage search results HTML.

    Args:
        html_content (str): The HTML content of the search results page.
        show_name (str): The name of the show to filter the results by.

    Returns:
        List[str]: A list of URLs for the 'More Info' buttons related to the specified show.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    search_results_container = soup.find("div", id="search-results-container")
    if not search_results_container:
        return []
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
            print(f"skipping {article_title}")
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
        print(f"{len(more_info_urls)} info urls: {more_info_urls}")
    else:
        print("no info urls")
    return more_info_urls


def extract_details_from_info_page(show_name: str, show_info_page_html: str) -> Tuple[str, str]:
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
    try:
        canonical_link = soup.find("link", rel="canonical")
        if canonical_link and canonical_link.get("href"):
            info_url = canonical_link["href"]
        else:
            og_url = soup.find("meta", property="og:url")
            if og_url and og_url.get("content"):
                info_url = og_url["content"]
    except Exception as e:
        print(f"error extracting info_url for show: {show_name}")
        print(str(e.with_traceback))
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
    except Exception as e:
        print(f"error extracting dates for show: {show_name}")
        print(str(e.with_traceback))
    try:
        location_section = soup.find("div", class_="location-section")
        if location_section:
            block_detail_div = location_section.find("div", class_="block-detail")
            if block_detail_div:
                venue_link_tag = block_detail_div.find("a")
                if venue_link_tag:
                    venue_name = venue_link_tag.get_text(strip=True)
                    venue_url = venue_link_tag.get("href")
    except Exception as e:
        print(f"error extracting location for show: {show_name}")
        print(e.with_traceback)
    result = (
        f"show: {show_name}"
        + f" first preview: {first_preview} "
        + f" date: {opening_night} to {closing_night}"
        + f" venue: {venue_name} url: {venue_url} "
        + f" extracted from: {info_url}"
        + f" {os.linesep}"
        + f" {os.linesep}"
    )
    html_result = f"""
        <div style="border:3px solid #e67e22; border-radius:16px; padding:24px; margin-bottom:32px; font-family:'Segoe UI', 'Arial', 'Helvetica Neue', Arial, sans-serif; background:linear-gradient(135deg,#fffbe6 0%,#ffe0b2 100%); box-shadow:0 4px 24px rgba(230,126,34,0.15);">
            <h2 style="margin-top:0; color:#c0392b; font-size:2em; letter-spacing:1px; text-shadow:1px 1px 0 #f9ca24, 2px 2px 0 #e67e22; font-family:'Segoe UI', Arial, sans-serif;">🎭 {show_name} 🎶</h2>
            <ul style="list-style:none; padding-left:0; font-size:1.05em;">
                <li style="margin-bottom:8px;"><strong style="color:#8e44ad;">First Preview:</strong> <span style="color:#2d3436;">{first_preview}</span></li>
                <li style="margin-bottom:8px;"><strong style="color:#16a085;">Opening Night:</strong> <span style="color:#2d3436;">{opening_night}</span></li>
                <li style="margin-bottom:8px;"><strong style="color:#d35400;">Closing Night:</strong> <span style="color:#2d3436;">{closing_night}</span></li>
                <li style="margin-bottom:8px;"><strong style="color:#2980b9;">Venue:</strong> <a href="{venue_url}" style="color:#e84393; font-weight:bold; text-decoration:underline;">{venue_name}</a></li>
                <li><strong style="color:#e67e22;">More Info:</strong> <a href="{info_url}" style="color:#27ae60; font-weight:bold; background:#fff3e0; padding:4px 10px; border-radius:6px; text-decoration:none; box-shadow:1px 1px 0 #e67e22;">Show Page</a></li>
            </ul>
        </div>
        """
    return result, html_result


def get_show_page(show_name: str) -> str:
    """
    Retrieves the HTML content of the search results page for a given show name from WhatsOnStage.

    Args:
        show_name (str): The name of the show to search for.

    Returns:
        str: The HTML content of the search results page.
    """
    query_url = f"https://www.whatsonstage.com/?s={show_name.replace(' ','+')}"
    show_page = requests.get(query_url, timeout=30).text
    return show_page


def get_info_page(info_url: str) -> str:
    """
    Retrieves the HTML content of a show's info page from WhatsOnStage.

    Args:
        info_url (str): The URL of the show's info page.

    Returns:
        str: The HTML content of the info page.
    """
    return requests.get(info_url, timeout=30).text


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
        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]}]"
            f" searching show {show_name}..."
        )
        show_page_html = get_show_page(show_name)
        info_urls = extract_info_links(show_page_html, show_name)
        for info_url in info_urls:
            show_info_page_html = get_info_page(info_url)
            text_result, html_result = extract_details_from_info_page(
                show_name, show_info_page_html
            )
            result += text_result
            html_aggregate += html_result
    html_report = (
        "<!DOCTYPE html>\n"
        "<html lang='en'>\n"
        "<head>\n"
        "  <meta charset='UTF-8'>\n"
        "  <meta name='viewport' content='width=device-width, initial-scale=1.0'>\n"
        "  <title>Sondheim Shows Weekly Report</title>\n"
        "</head>\n"
        "<body style='background:#f4f6f8; margin:0; padding:32px;'>\n"
        f"{html_aggregate}\n"
        "</body>\n"
        "</html>\n"
    )
    return result, html_report


def test_flow() -> None:
    """
    full flow
    """
    result_tuple = search_shows(SHOWS)
    result, html_report = result_tuple
    filename = f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_report.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_report)
    print(f"HTML report saved to {filename}")
    print("-" * 30)
    print(html_report)
    print("-" * 30)
    print(result)
    print("-" * 30)


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
    Reads a local HTML file, extracts 'More Info' links for the show "The Frogs",
    and prints the result.
    """
    with open("./obs/wos_info.html", "r", encoding="utf-8") as f:
        html_content_from_file = f.read()
        result = extract_details_from_info_page(
            "The Frogs", html_content_from_file
        )
        print(result)
