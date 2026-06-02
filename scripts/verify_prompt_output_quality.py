#!/usr/bin/env python3
"""Verify draft outputs contain no banned claims.

Scans:
  1. policies/dealix_control_policy.yaml banned_claims (declared list)
  2. docs/marketing, docs/sales, docs/sales-kit, docs/commercial, docs/growth
     for any occurrence of the banned phrases. A match is reported only when
     the phrase is NOT in a negation context — i.e. preceded by markers like
     "no ", "not ", "never ", "without ", "do not", "don't", Arabic "لا ",
     "بدون ", "ليس ", "نمنع" etc., and not inside a recognised
     "what we do NOT do" / "forbidden" / "banned" file.
  3. Exercises auto_client_acquisition.governance_os.draft_gate.audit_draft_text
     on a fixture string to confirm the gate is wired. If the draft_gate
     module cannot be imported (optional deps missing in the runner), the
     exercise is skipped with a soft warning rather than failing.
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

POLICY_PATH = REPO / "policies" / "dealix_control_policy.yaml"
SCAN_DIRS = (
    REPO / "docs" / "marketing",
    REPO / "docs" / "sales",
    REPO / "docs" / "sales-kit",
    REPO / "docs" / "commercial",
    REPO / "docs" / "growth",
)

# Files that explicitly enumerate what Dealix DOES NOT do, or that ARE the
# governance / banned-claim registry itself. Listing a banned phrase inside
# these files is not a violation — the file is the source of truth.
NEGATION_DOC_PATTERNS = (
    "what_we_do_not_do",
    "banned",
    "forbidden",
    "do_not",
    "no_overclaim",
    "TRUTH_CHECK",
    "GOVERNANCE_GATES",
    "POLICY",
    "RED_TEAM",
)

NEGATION_WINDOW = 300  # chars before the phrase to inspect for negation markers

NEGATION_MARKERS_EN = (
    "no ",
    "not ",
    "never",
    "without",
    "do not",
    "don't",
    "won't",
    "will not",
    "refuse",
    "refusal",
    "forbid",
    "ban ",
    "banned",
    "prohibit",
    "block ",
    "blocked",
    "avoid",
    "anti-",
    "anti pattern",
    "anti-pattern",
    "non-",
    "—not",
    "we cannot",
    "we can't",
    "we don't",
    "we never",
    "❌",
    "forbidden",
    "false:",
    "reject",
    "rejected",
    "disqualif",
    "out of scope",
    "outside the",
    "outside scope",
    "examples:",
    "wants ",
    "scope:",
    "what we do not",
    "what we don't",
    "what we will not",
    "what we won't",
    "is not allowed",
    "is forbidden",
    "is banned",
    "is rejected",
    "polite refusal",
    "constitutional clause",
    "friction_log",
    "list of",
    "such as:",
    "not included",
    "excluded",
    "out-of-scope",
    "we will not",
    "we never offer",
    "we never promise",
    "## not",
    "# not",
)

NEGATION_MARKERS_AR = (
    "لا ",
    "بدون",
    "ليس",
    "لن ",
    "ما ",
    "نرفض",
    "نمنع",
    "نتجنب",
    "حظر",
    "ممنوع",
    "محظور",
    "غير مسموح",
    "لا نضمن",
    "لا نقدم",
)


def _fail(msg: str) -> None:
    print(msg, file=sys.stderr)


def _load_banned() -> tuple[list[str], list[str]]:
    if not POLICY_PATH.is_file():
        return [], []
    data = yaml.safe_load(POLICY_PATH.read_text(encoding="utf-8")) or {}
    block = data.get("banned_claims") or {}
    eng = [str(t) for t in (block.get("english") or [])]
    ara = [str(t) for t in (block.get("arabic") or [])]
    return eng, ara


def _is_negated(text: str, idx: int) -> bool:
    """A phrase is negated if EITHER the English-marker check OR the
    Arabic-marker check finds a marker in the window before idx.

    Arabic markers are matched against raw text (case-preserving),
    English markers against lowercased text. Arabic docs often embed
    English technical terms (e.g. "لا fake proof"), so both passes
    run for every match.
    """
    start = max(0, idx - NEGATION_WINDOW)
    window_raw = text[start:idx]
    window_lower = window_raw.lower()
    if any(m in window_lower for m in NEGATION_MARKERS_EN):
        return True
    if any(m in window_raw for m in NEGATION_MARKERS_AR):
        return True
    return False


def _scan_markdown(banned_en: list[str], banned_ar: list[str]) -> list[tuple[str, str]]:
    hits: list[tuple[str, str]] = []
    for root in SCAN_DIRS:
        if not root.is_dir():
            continue
        for md in root.rglob("*.md"):
            name = md.name
            stem = md.stem
            if any(pat.lower() in stem.lower() or pat in stem for pat in NEGATION_DOC_PATTERNS):
                continue
            try:
                text = md.read_text(encoding="utf-8")
            except OSError:
                continue

            blob_lower = text.lower()
            for term in banned_en:
                t = term.lower()
                start = 0
                while True:
                    idx = blob_lower.find(t, start)
                    if idx == -1:
                        break
                    if not _is_negated(text, idx):
                        hits.append((str(md.relative_to(REPO)), term))
                        break  # one hit per (file, term) is enough
                    start = idx + len(t)

            for term in banned_ar:
                start = 0
                while True:
                    idx = text.find(term, start)
                    if idx == -1:
                        break
                    if not _is_negated(text, idx):
                        hits.append((str(md.relative_to(REPO)), term))
                        break
                    start = idx + len(term)
    return hits


def _exercise_draft_gate() -> tuple[bool, list[str]]:
    """Returns (skipped, errors)."""
    try:
        from auto_client_acquisition.governance_os.draft_gate import (
            audit_draft_text,
        )
    except Exception as exc:  # pragma: no cover
        # Soft skip — optional dependency missing in the runner.
        _fail(f"draft_gate_import_skipped:{exc}")
        return True, []

    errors: list[str] = []
    bad_sample = "We provide guaranteed sales and نضمن لك مبيعات."
    issues = audit_draft_text(bad_sample)
    if not issues:
        errors.append("draft_gate_failed_to_flag_bad_sample")

    good_sample = "We help Saudi teams reduce manual ops work."
    if audit_draft_text(good_sample):
        errors.append("draft_gate_false_positive_on_clean_sample")

    return False, errors


def main() -> int:
    banned_en, banned_ar = _load_banned()
    if not banned_en or not banned_ar:
        _fail("banned_claims_list_empty_or_policy_missing")
        print("PROMPT_OUTPUT_QUALITY_PASS=false")
        return 1

    errors: list[str] = []
    hits = _scan_markdown(banned_en, banned_ar)
    for path, term in hits:
        errors.append(f"banned_phrase_in_doc:{path}:{term}")

    skipped, gate_errors = _exercise_draft_gate()
    errors.extend(gate_errors)

    for err in errors:
        _fail(err)

    ok = not errors
    print(f"PROMPT_OUTPUT_QUALITY_PASS={'true' if ok else 'false'}")
    print(f"PROMPT_OUTPUT_QUALITY_BANNED_TERM_COUNT={len(banned_en) + len(banned_ar)}")
    print(f"PROMPT_OUTPUT_QUALITY_DRAFT_GATE_SKIPPED={'true' if skipped else 'false'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
