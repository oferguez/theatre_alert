"""
search WhatsOnStage.com for all Sondheim shows,
extract info for each and compile a weekly email report
"""

import re
import requests
from typing import List

from bs4 import BeautifulSoup, Tag
import os

shows: List[str] = [
        'Here We Are',

        'Saturday Night',
        'Candide',
        'West Side Story',
        'Gypsy',
        'A Funny Thing Happened on the Way to the Forum',
        'Anyone Can Whistle',
        'Do I Hear a Waltz?',
        'The Mad Show',
        'Evening Primrose',
        'Company',
        'Follies',
        'A Little Night Music',
        'The Frogs',
        'Pacific Overtures',
        'Side by Side by Sondheim',
        'Sweeney Todd',
        'Marry Me a Little',
        'Merrily We Roll Along',
        'Sunday in the Park with George',
        'Into the Woods',
        'Assassins',
        'Putting It Together',
        'Passion',
        'Road Show',
        'Here We Are',
        'Hot Spot'
        ]


def extract_info_links(html_content: str, show_name: str) -> List[str]:
    """
    Parses the HTML content to find 'More Info' links related to a specific show
    and extract their href.

    Args:
        html_content (str): The HTML content of the search results page.
        show_name (str): The name of the show to filter the results by.

    Returns:
        list: A list of URLs for the 'More Info' buttons related to the specified show.
    """
    soup: BeautifulSoup = BeautifulSoup(html_content, "html.parser")

    search_results_container: Optional[Tag] = soup.find("div", id="search-results-container")

    if not search_results_container:
        return []

    articles: List[Tag] = search_results_container.find_all("article", class_="col-12")

    more_info_urls: List[str] = []

    article: Tag
    for article in articles:
        type_link_tag: Optional[Tag] = article.find("a", class_="text-body-tertiary")
        if not type_link_tag or type_link_tag.get_text(strip=True).upper() != "SHOW":
            continue
        article_title_tag: Optional[Tag] = article.find("h3", class_="fw-bold").find("a")
        if not article_title_tag:
            continue

        article_title: str = article_title_tag.get_text(strip=True)
        if not re.search(re.escape(show_name), article_title, re.IGNORECASE):
            continue
        more_info_links_in_article: List[Tag] = article.find_all("a", class_="buy-tickets-link")
        link: Tag
        for link in more_info_links_in_article:
            span_tag: Optional[Tag] = link.find("span", string="More Info")
            if span_tag:
                href: Optional[str] = link.get("href")
                if href:
                    more_info_urls.append(href)
                break
    return more_info_urls

def extract_show_info(info_url: str) -> str:
    return info_url + os.linesep

def get_show_page(show_name: str) -> str:
    """
    extract show page html
    """
    result:str = ""
    query_url:str = f"https://www.whatsonstage.com/?s={show_name.replace(' ','+')}" 
    show_page:str = requests.get(query_url, timeout=30)
    info_pages:List[str] = extract_info_links(show_page, show_name)
    for info_page:str in info_pages:
        result += extract_show_info(info_page)
    return result


def search_shows(shows:List[str]) -> str:
    for show in shows:
        info_urls:List[str] = extract_info_links(show)

if __name__ == "__main__":
    with open("./obs/wos.html", "r", encoding="utf-8") as f:
        html_content_from_file = f.read()
        result = extract_info_links(html_content_from_file, "The Frogs")
        print(f"result: {result}")
