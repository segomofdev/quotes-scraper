# Quotes Scraper — JavaScript-Rendered Site (Python + Selenium)

A small, production-style web scraper that extracts data from a
**JavaScript-rendered** website and exports it to clean CSV and JSON.

The target site renders its content with JavaScript, so a plain HTTP request
returns an empty page — this scraper drives a real headless Chrome browser
with **Selenium** to render and extract the data, the same way a production
scraping system would.

Built to demonstrate not just "a script that works once," but the engineering
practices that keep a scraper reliable over time: the **Page Object pattern**,
explicit waits, retry logic, containerization, and **CI/CD**.

---

## Features

- **Handles JS-rendered content** — Selenium + headless Chrome, explicit waits
  (no brittle `time.sleep` guessing for element loading)
- **Full pagination** — follows "next" links until the last page
- **Page Object pattern** — selectors and page logic isolated in one place, so
  markup changes touch only a single file
- **Retry & back-off** — transient failures are retried before giving up
- **Polite crawling** — configurable delay between requests
- **Clean exports** — deduplicated, structured **CSV** and **JSON**
- **Dockerized** — runs anywhere, no local Chrome setup needed
- **CI/CD** — GitHub Actions runs the scraper on a schedule and publishes the
  results as a downloadable artifact

---

## Tech stack

`Python 3.12` · `Selenium 4` · `Docker` · `GitHub Actions`

---

## Project structure

```
quotes-scraper/
├── scraper/
│   ├── main.py            # entry point / orchestration
│   ├── config.py          # all tunable settings
│   ├── driver.py          # configured headless Chrome
│   ├── models.py          # typed data model (dataclass)
│   ├── exporters.py       # CSV + JSON output
│   └── pages/
│       └── quotes_page.py # Page Object: selectors + page actions
├── .github/workflows/scrape.yml   # CI: scheduled run + artifact upload
├── Dockerfile
├── requirements.txt
└── output/                # results land here
```

---

## Quick start

### Local

```bash
git clone https://github.com/segomofdev/quotes-scraper.git
cd quotes-scraper
pip install -r requirements.txt
python -m scraper.main
```

Results appear in `output/quotes.json` and `output/quotes.csv`.

Watch it run in a real browser window:

```bash
python -m scraper.main --no-headless
```

### Docker

```bash
docker build -t quotes-scraper .
docker run --rm -v "$(pwd)/output:/app/output" quotes-scraper
```

---

## Example output

`output/quotes.json`:

```json
[
  {
    "text": "It is our choices, Harry, that show what we truly are, far more than our abilities.",
    "author": "J.K. Rowling",
    "tags": ["abilities", "choices"]
  }
]
```

(See `output/quotes.sample.json` and `output/quotes.sample.csv` for full samples.)

---

## How it adapts to other sites

The scraper is structured so that targeting a different site means editing
**one file** — `scraper/pages/quotes_page.py` — to update the selectors and the
data model. The browser handling, retry logic, pagination loop, and exporters
stay the same. This is the difference between a throwaway script and a
maintainable scraper.

---

## Notes

This project targets [`quotes.toscrape.com`](https://quotes.toscrape.com/js/),
a public sandbox built specifically for practicing web scraping. Always review
a site's Terms of Service and `robots.txt` before scraping, and crawl
respectfully (rate limiting is built in here).
