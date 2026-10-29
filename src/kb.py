"""Knowledge base loader and source selection.

The KB is small (12 files), so there is no vector database. Sources are picked
by issue type plus a few keywords, and the selected ids are returned so the
pipeline can log what the model was given.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

KB_DIR = Path(__file__).resolve().parent.parent / "kb"

# Always provided: tells the model what the KB does NOT cover (recalls,
# used-item denials, fraud criteria, KB 710 status).
ALWAYS_INCLUDED = ("NOTE-KNOWLEDGE-QUALITY",)

SOURCES_BY_ISSUE_TYPE = {
    "return": ("POL-RETURN", "KB-101"),
    "exchange": ("POL-RETURN", "KB-101"),
    "refund": ("POL-RETURN", "KB-101"),
    "damaged": ("POL-RETURN", "KB-101"),
    "wrong_item": ("POL-RETURN",),
    "missing_shipment": ("POL-SHIPPING", "KB-205"),
    "shipping_delay": ("POL-SHIPPING",),
    "warranty": ("POL-WARRANTY-SAFETY", "KB-318"),
    "product_safety": ("POL-WARRANTY-SAFETY", "KB-427", "KB-318"),
    "chargeback": ("POL-RETURN",),
    "fraud_signal": ("POL-RETURN",),
    "account_change": ("POL-SHIPPING", "KB-710"),
    "product_question": (),
    "other": (),
}

SOURCES_BY_KEYWORD = (
    (r"carabiner|harness|rope|helmet|belay|climbing|protective", ("POL-WARRANTY-SAFETY", "KB-427")),
    (r"wash|waterproof|rain shell|tags? removed", ("KB-510",)),
    (r"stove", ("KB-612",)),
    (r"address", ("KB-710",)),
    (r"delivered|parcel|package", ("KB-205",)),
)


@dataclass(frozen=True)
class KBSource:
    id: str
    title: str
    type: str  # policy | kb | note
    source_section: str
    last_reviewed: str
    owner: str
    authoritative: bool
    body: str


def _parse(path: Path) -> KBSource:
    text = path.read_text(encoding="utf-8")
    _, header, body = text.split("---", 2)
    meta = dict(line.split(": ", 1) for line in header.strip().splitlines())
    return KBSource(
        id=meta["id"],
        title=meta["title"],
        type=meta["type"],
        source_section=meta["source_section"],
        last_reviewed=meta["last_reviewed"],
        owner=meta["owner"],
        authoritative=meta["authoritative"] == "true",
        body=body.strip(),
    )


def load_kb(kb_dir: Path = KB_DIR) -> dict[str, KBSource]:
    sources = (_parse(p) for p in sorted(kb_dir.glob("*.md")))
    return {s.id: s for s in sources}


def select_sources(issue_type: str | None, text: str = "") -> tuple[str, ...]:
    """Return KB ids relevant to a case, in a stable order without duplicates."""
    ids = list(ALWAYS_INCLUDED)
    ids += SOURCES_BY_ISSUE_TYPE.get(issue_type or "other", ())
    for pattern, kb_ids in SOURCES_BY_KEYWORD:
        if re.search(pattern, text, re.IGNORECASE):
            ids += kb_ids
    return tuple(dict.fromkeys(ids))
