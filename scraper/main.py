"""Entry point: crawl every page of the target site and export the results.

Usage:
    python -m scraper.main
    python -m scraper.main --no-headless     # watch it run in a real window
"""
from __future__ import annotations

import argparse
import logging
import time

from selenium.common.exceptions import TimeoutException, WebDriverException

from .config import settings
from .driver import build_driver
from .exporters import to_csv, to_json
from .models import Quote
from .pages.quotes_page import QuotesPage

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("scraper")


def scrape_all() -> list[Quote]:
    driver = build_driver(headless=settings.headless)
    all_quotes: list[Quote] = []
    try:
        page = QuotesPage(driver, settings.wait_timeout)
        url: str | None = settings.base_url
        page_no = 1

        while url:
            for attempt in range(1, settings.max_retries + 1):
                try:
                    page.load(url)
                    break
                except (TimeoutException, WebDriverException) as exc:
                    log.warning(
                        "Page %d failed (attempt %d/%d): %s",
                        page_no, attempt, settings.max_retries, exc,
                    )
                    if attempt == settings.max_retries:
                        raise
                    time.sleep(settings.request_delay * attempt)

            all_quotes.extend(page.extract_quotes())
            url = page.next_page_url()
            page_no += 1
            if url:
                time.sleep(settings.request_delay)  # be polite

        log.info("Done. Collected %d quotes across %d pages.",
                 len(all_quotes), page_no - 1)
        return all_quotes
    finally:
        driver.quit()


def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape quotes (JS-rendered).")
    parser.add_argument("--no-headless", action="store_true",
                        help="Run with a visible browser window.")
    args = parser.parse_args()
    if args.no_headless:
        object.__setattr__(settings, "headless", False)

    quotes = scrape_all()
    to_json(quotes, settings.output_dir / "quotes.json")
    to_csv(quotes, settings.output_dir / "quotes.csv")


if __name__ == "__main__":
    main()
