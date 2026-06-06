"""Write scraped records to CSV and JSON."""
from __future__ import annotations

import csv
import json
import logging
from pathlib import Path

from .models import Quote

log = logging.getLogger(__name__)


def to_json(quotes: list[Quote], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump([q.as_dict() for q in quotes], fh, ensure_ascii=False, indent=2)
    log.info("Wrote %d records to %s", len(quotes), path)


def to_csv(quotes: list[Quote], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["text", "author", "tags"])
        for q in quotes:
            writer.writerow([q.text, q.author, "; ".join(q.tags)])
    log.info("Wrote %d records to %s", len(quotes), path)
