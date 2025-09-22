"""
pytest -v tests/unittests/test_unit_wos_sondheim_alert.py
"""

import pytest
import main


@pytest.fixture
def show_name():
    return "The Frogs"


@pytest.fixture
def html_with_link():
    return """
    <div id="search-results-container">
      <article class="col-12">
        <a class="text-body-tertiary">SHOW</a>
        <h3 class="fw-bold"><a>The Frogs</a></h3>
        <a class="buy-tickets-link" href="/show/the-frogs-info"><span>More Info</span></a>
      </article>
    </div>
    """


@pytest.fixture
def html_info_page():
    return """
    <html>
      <head>
        <link rel="canonical" href="https://www.whatsonstage.com/show/the-frogs-info" />
      </head>
      <body>
        <div class="dates-section">
          <p>First Preview 2025-07-01</p>
          <p>Opening Night 2025-07-05</p>
          <p>Closing Night 2025-08-01</p>
        </div>
        <div class="location-section">
          <div class="block-detail">
            <a href="https://venue.example.com">Frogs Theatre</a>
          </div>
        </div>
      </body>
    </html>
    """


def test_extract_info_links(html_with_link, show_name):
    result, log = main.extract_info_links(html_with_link, show_name)
    assert isinstance(result, list)
    assert any("frogs-info" in link for link in result)
    assert "found" in log or "no show info links" in log


def test_extract_details_from_info_page(html_info_page, show_name):
    text_result, html_result = main.extract_details_from_info_page(
        show_name, html_info_page
    )
    assert isinstance(text_result, str)
    assert "The Frogs" in text_result
    assert "First Preview" in html_result
    assert "Frogs Theatre" in html_result


def test_search_shows(monkeypatch, show_name, html_with_link, html_info_page):
    # Patch network calls to use our HTML fixtures
    def fake_get_show_page(name):
        return html_with_link

    def fake_get_info_page(url):
        return html_info_page, ""

    monkeypatch.setattr(main, "get_show_page", fake_get_show_page)
    monkeypatch.setattr(main, "get_info_page", fake_get_info_page)
    result, html_report = main.search_shows([show_name])
    assert isinstance(result, str)
    assert isinstance(html_report, str)
    assert "The Frogs" in result
    assert "The Frogs" in html_report
