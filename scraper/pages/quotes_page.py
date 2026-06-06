"""Page Object for the quotes listing page.

The Page Object pattern keeps selectors and page interactions in one place,
isolated from the scraping orchestration. If the site's markup changes, this
is the only file that needs editing.
"""
from __future__ import annotations

import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ..models import Quote

log = logging.getLogger(__name__)


class QuotesPage:
    """Represents a single paginated page of quotes."""

    # --- Locators -------------------------------------------------------
    _QUOTE = (By.CSS_SELECTOR, "div.quote")
    _TEXT = (By.CSS_SELECTOR, "span.text")
    _AUTHOR = (By.CSS_SELECTOR, "small.author")
    _TAG = (By.CSS_SELECTOR, "div.tags a.tag")
    _NEXT = (By.CSS_SELECTOR, "li.next > a")

    def __init__(self, driver: WebDriver, timeout: int) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def load(self, url: str) -> None:
        log.info("Loading %s", url)
        self.driver.get(url)
        # Quotes are injected by JavaScript, so wait for them to appear
        # rather than reading raw HTML (which would be empty).
        self.wait.until(EC.presence_of_element_located(self._QUOTE))

    def extract_quotes(self) -> list[Quote]:
        cards = self.driver.find_elements(*self._QUOTE)
        quotes: list[Quote] = []
        for card in cards:
            text = card.find_element(*self._TEXT).text.strip().strip("\u201c\u201d\"")
            author = card.find_element(*self._AUTHOR).text.strip()
            tags = [t.text.strip() for t in card.find_elements(*self._TAG)]
            quotes.append(Quote(text=text, author=author, tags=tags))
        log.info("Extracted %d quotes from current page", len(quotes))
        return quotes

    def next_page_url(self) -> str | None:
        """Return the absolute URL of the next page, or None if last page."""
        links = self.driver.find_elements(*self._NEXT)
        if not links:
            return None
        return links[0].get_attribute("href")
