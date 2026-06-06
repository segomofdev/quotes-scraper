"""Typed data model for a scraped record."""
from __future__ import annotations

from dataclasses import dataclass, field, asdict


@dataclass
class Quote:
    text: str
    author: str
    tags: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        return asdict(self)
