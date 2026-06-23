"""Shared text scanner for Wave 8 verifiers.

Finds genuine unsafe-claim / auto-send phrasing while ignoring lines that
appear inside a *prohibition* context (e.g. a "We never do:" list or a
"لا auto-send" rule). Prohibition is detected by scanning the matching line
plus a look-back window of preceding non-empty lines for a negation cue.
"""
from __future__ import annotations

import re

# Cues that indicate the surrounding text *forbids* the phrase rather than
# claiming it. English + Arabic.
PROHIBITION_CUES = (
    "no ", "not ", "never", "don't", "do not", "does not", "avoid",
    "without", "forbidden", "prohibit", "ban ", "we do not", "we don't",
    "must not", "may not", "لا ", "ممنوع", "بدون", "نتجنب", "خوف",
    "نحن لا", "يمنع", "غير مسموح",
)


def _has_cue(line: str) -> bool:
    low = line.lower()
    return any(cue in low for cue in PROHIBITION_CUES)


def scan_text(text: str, patterns: tuple[str, ...], lookback: int = 6) -> list[str]:
    """Return matching lines that are NOT in a prohibition context."""
    compiled = [re.compile(p, re.IGNORECASE) for p in patterns]
    lines = text.splitlines()
    nonempty_prev: list[str] = []  # rolling window of preceding non-empty lines
    hits: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if any(rx.search(line) for rx in compiled):
            window = [*nonempty_prev[-lookback:], line]
            if not any(_has_cue(w) for w in window):
                hits.append(stripped[:120])
        nonempty_prev.append(line)
    return hits


def scan_files(repo, rels: tuple[str, ...], patterns: tuple[str, ...], lookback: int = 6) -> list[str]:
    hits: list[str] = []
    for rel in rels:
        fp = repo / rel
        if not fp.is_file():
            continue
        text = fp.read_text(encoding="utf-8", errors="ignore")
        for h in scan_text(text, patterns, lookback=lookback):
            hits.append(f"{rel}: {h}")
    return hits
