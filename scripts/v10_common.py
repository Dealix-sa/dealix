#!/usr/bin/env python3
"""Shared helpers for Dealix V10 Institutional Scale & Market Domination OS.

Pure-stdlib utilities used by V10 verification and generation scripts:

* repo path resolution
* required-file presence checks
* required-marker (substring) checks inside docs
* a forbidden-claims guard (no guaranteed ROI / fake traction / unverified claims)
* small JSON + verdict helpers

Nothing here sends anything externally. Everything is read / score / report only.
"""

from __future__ import annotations

import json
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

# Claims that must never appear in V10 customer-facing or governance docs.
# Mirrors the non-negotiables: no guaranteed ROI, no fake traction, no
# unverified claims, no fake security/compliance certifications.
FORBIDDEN_CLAIMS = (
    "guaranteed roi",
    "guaranteed return",
    "roi مضمون",
    "عائد مضمون",
    "نتائج مضمونة",
    "guaranteed results",
    "iso 27001 certified",
    "soc 2 certified",
    "soc2 certified",
    "fully compliant",
    "100% secure",
    "امتثال كامل مضمون",
)

# The unbreakable rule, embedded into every V10 document.
NON_NEGOTIABLE_AR = (
    "AI يجهّز ويحلّل ويصيغ ويُقيّم ويرتّب ويوصي. "
    "المؤسس يراجع ويعتمد ويوقّع ويبيع ويرسل يدويًا ويقرر. "
    "النظام لا يرسل خارجيًا أبدًا."
)


@dataclass
class CheckResult:
    """Outcome of a single verification pass."""

    name: str
    required_files: list[str] = field(default_factory=list)
    missing_files: list[str] = field(default_factory=list)
    missing_markers: list[str] = field(default_factory=list)
    forbidden_hits: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not (self.missing_files or self.missing_markers or self.forbidden_hits)

    @property
    def verdict(self) -> str:
        return "PASS" if self.passed else "FAIL"

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "verdict": self.verdict,
            "required_file_count": len(self.required_files),
            "present_file_count": len(self.required_files) - len(self.missing_files),
            "missing_files": self.missing_files,
            "missing_markers": self.missing_markers,
            "forbidden_hits": self.forbidden_hits,
        }


def check_files(paths: Iterable[str]) -> list[str]:
    """Return the subset of *paths* (repo-relative) that do not exist."""
    missing = []
    for rel in paths:
        if not (REPO / rel).is_file():
            missing.append(rel)
    return missing


def check_markers(rel_path: str, markers: Iterable[str]) -> list[str]:
    """Return markers not present in the given file (empty if file missing handled by caller)."""
    p = REPO / rel_path
    if not p.is_file():
        return list(markers)
    text = p.read_text(encoding="utf-8")
    return [m for m in markers if m not in text]


# Negation tokens — a forbidden phrase preceded by one of these is a POLICY
# statement ("no guaranteed ROI"), not a claim, and must not be flagged.
_NEGATORS = (
    "لا ",
    "بدون",
    "دون ",
    "ممنوع",
    "غير ",
    "نمنع",
    "يمنع",
    "no ",
    "not ",
    "never",
    "without",
    "prohibit",
    "forbidden",
    "ban ",
    "avoid",
)


def _is_negated(text_low: str, idx: int, window: int = 28) -> bool:
    """True if a negation token appears shortly before position *idx*."""
    start = max(0, idx - window)
    before = text_low[start:idx]
    return any(neg in before for neg in _NEGATORS)


def scan_forbidden(paths: Iterable[str]) -> list[str]:
    """Return 'file::phrase' entries where a forbidden claim appears AFFIRMATIVELY.

    Negation-aware: prohibitive statements such as "لا ROI مضمون" / "no guaranteed
    roi" are policy text and are not flagged.
    """
    hits = []
    for rel in paths:
        p = REPO / rel
        if not p.is_file():
            continue
        low = p.read_text(encoding="utf-8").lower()
        for phrase in FORBIDDEN_CLAIMS:
            start = 0
            while True:
                idx = low.find(phrase, start)
                if idx == -1:
                    break
                if not _is_negated(low, idx):
                    hits.append(f"{rel}::{phrase}")
                    break
                start = idx + len(phrase)
    return hits


def run_check(
    name: str,
    required_files: list[str],
    markers: dict[str, list[str]] | None = None,
    forbidden_scan: bool = True,
) -> CheckResult:
    """Run a full check: presence + per-file markers + forbidden-claim scan."""
    missing_files = check_files(required_files)
    missing_markers: list[str] = []
    if markers:
        for rel, marks in markers.items():
            for missing in check_markers(rel, marks):
                missing_markers.append(f"{rel}::{missing}")
    forbidden_hits = scan_forbidden(required_files) if forbidden_scan else []
    return CheckResult(
        name=name,
        required_files=required_files,
        missing_files=missing_files,
        missing_markers=missing_markers,
        forbidden_hits=forbidden_hits,
    )


def write_json(rel_out: str, payload: dict) -> Path:
    """Write *payload* as pretty JSON to a repo-relative path, creating parents."""
    out = REPO / rel_out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return out


def emit(result: CheckResult, json_out: str | None = None) -> int:
    """Print a verdict block, optionally write JSON, return process exit code."""
    if json_out:
        write_json(json_out, result.to_dict())
    print(f"=== {result.name} VERDICT ===")
    print(f"VERDICT={result.verdict}")
    print(
        f"FILES_PRESENT={len(result.required_files) - len(result.missing_files)}/{len(result.required_files)}"
    )
    for m in result.missing_files:
        print(f"missing_file={m}")
    for m in result.missing_markers:
        print(f"missing_marker={m}")
    for h in result.forbidden_hits:
        print(f"forbidden_claim={h}")
    return 0 if result.passed else 1
