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

import datetime
import os
import re
from typing import List, Optional
import requests
from bs4 import BeautifulSoup, Tag

SHOWS: List[str] = [
    "Here We Are",
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
    soup: BeautifulSoup = BeautifulSoup(html_content, "html.parser")

    search_results_container: Optional[Tag] = soup.find(
        "div", id="search-results-container"
    )

    if not search_results_container:
        return []

    articles: List[Tag] = search_results_container.find_all("article", class_="col-12")

    more_info_urls: List[str] = []

    article: Tag
    for article in articles:
        type_link_tag: Optional[Tag] = article.find("a", class_="text-body-tertiary")
        if not type_link_tag or type_link_tag.get_text(strip=True).upper() != "SHOW":
            continue
        article_title_tag: Optional[Tag] = article.find("h3", class_="fw-bold").find(
            "a"
        )
        if not article_title_tag:
            continue

        article_title: str = article_title_tag.get_text(strip=True)
        if not re.search(re.escape(show_name), article_title, re.IGNORECASE):
            continue
        more_info_links_in_article: List[Tag] = article.find_all(
            "a", class_="buy-tickets-link"
        )
        link: Tag
        for link in more_info_links_in_article:
            span_tag: Optional[Tag] = link.find("span", string="More Info")
            if span_tag:
                href: Optional[str] = link.get("href")
                if href:
                    more_info_urls.append(href)
                break
    return more_info_urls


def extract_details_from_info_page(show_name: str, show_info_page_html: str) -> str:
    """
    Formats and returns details for a show from its info page HTML.

    Args:
        show_name (str): The name of the show.
        show_info_page_html (str): The HTML content of the show's info page.

    Returns:
        str: A formatted string containing the show name and info page details.
    """

    soup = BeautifulSoup(show_info_page_html, "html.parser")

    opening_night:str = "N/A"
    closing_night:str = "N/A"
    venue_name:str = "N/A"
    venue_url:str = "N/A"

    try:
        dates_section = soup.find(class_="dates-section")
        opening_night_p_tag = dates_section.find('p',\
                                                string=re.compile("opening night",\
                                                re.IGNORECASE))
        opening_night = opening_night_p_tag.text.strip()
        closing_night_p_tag = dates_section.find('p',\
                                                 string=re.compile("closing night",\
                                                 re.IGNORECASE))
        closing_night = closing_night_p_tag.text.strip()
    except Exception as e:
        print (f'error extracting dates for show: {show_name}')
        print(e.with_traceback)

    try:
        location_section = soup.find('div', class_='location-section')
        block_detail_div = location_section.find('div', class_='block-detail')
        venue_link_tag = block_detail_div.find('a')
        venue_name = venue_link_tag.get_text(strip=True)
        venue_url = venue_link_tag.get('href')
    except Exception as e:
        print (f'error extracting location for show: {show_name}')
        print(e.with_traceback)

    result = f"show: {show_name} " + \
             f" date: {opening_night} to {closing_night}" + \
             f" venue: {venue_name} url: {venue_url} " + \
             f" {os.linesep}"

    return result


def get_show_page(show_name: str) -> str:
    """
    Retrieves the HTML content of the search results page for a given show name from WhatsOnStage.

    Args:
        show_name (str): The name of the show to search for.

    Returns:
        str: The HTML content of the search results page.
    """
    query_url: str = f"https://www.whatsonstage.com/?s={show_name.replace(' ','+')}"
    show_page: str = requests.get(query_url, timeout=30).text
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


def search_shows(shows: List[str]) -> str:
    """
    Searches for each show in the provided list, extracts info URLs, and compiles the information.

    Args:
        shows (List[str]): A list of show names to search for.

    Returns:
        str: A compiled string of extracted show information for all shows.
    """
    result: str = ""
    for show_name in shows:
        now = time.time()
        seconds = int(now)
        milliseconds = int((now - seconds) * 1000)
        print(f"Time: {seconds}.{milliseconds:03d} s")
        print(f'[{datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]}] searching show {show_name}...')
        show_page_html: str = get_show_page(show_name)
        info_urls: List[str] = extract_info_links(show_page_html, show_name)
        for info_url in info_urls:
            show_info_page_html: str = get_info_page(info_url)
            result += extract_details_from_info_page(show_name, show_info_page_html)
    return result

def test_flow() -> None:
    """
    full flow
    """
    result: str = search_shows(SHOWS)
    print(result)


if __name__ == "__main__":
    test_flow()




def test_html_parser_show_page():
    """
    Reads a local HTML file, extracts 'More Info' links for the show "The Frogs",
    and prints the result.
    """
    with open("./obs/wos.html", "r", encoding="utf-8") as f:
        html_content_from_file = f.read()
        result = extract_info_links(html_content_from_file, "The Frogs")
        print(f"result: {result}")

def test_html_parser_show_info():
    """
    Reads a local HTML file, extracts 'More Info' links for the show "The Frogs",
    and prints the result.
    """
    with open('./obs/wos_info.html', 'r', encoding='utf-8') as f:
        html_content_from_file = f.read()
        result:str = extract_details_from_info_page("The Frogs", html_content_from_file)
        print(result)
