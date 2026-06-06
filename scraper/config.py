"""Central configuration for the scraper.

All tunable values live here so the rest of the code stays clean and the
behaviour can be changed without touching logic.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    # Target site (a public sandbox built specifically for scraping practice).
    base_url: str = "https://quotes.toscrape.com/js/"

    # Run the browser without a visible window. Keep True for servers/CI.
    headless: bool = True

    # Seconds to wait for elements before giving up.
    wait_timeout: int = 15

    # How many times to retry loading a page that fails.
    max_retries: int = 3

    # Polite delay between page requests (seconds). Don't hammer servers.
    request_delay: float = 1.0

    # Where results are written.
    output_dir: Path = Path("output")


settings = Settings()
