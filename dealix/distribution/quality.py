"""Draft Quality Gate — deterministic checks before a draft can be approved.

Hard rules (errors → draft fails the gate):
  - no banned / overclaim phrase (نضمن / guaranteed / blast / إرسال جماعي ...)
  - operating mode is ``draft_only_no_auto_send``
  - status is a known draft status
  - evidence_level is a valid 0–5 integer
  - a CTA is present (one clear next action)
  - Arabic body present and within sane length bounds
  - passes the JSON schema

Soft rules (warnings → surfaced, not blocking):
  - too many distinct asks (more than 3 question marks)
  - contains a raw URL (drafts are copied + sent manually; links are added by the founder)
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from dealix.distribution.doctrine import (
    OPERATING_MODE,
    STATUS_APPROVED,
    STATUS_COPIED,
    STATUS_PENDING,
    STATUS_REJECTED,
    scan_text_for_banned_claims,
)
from dealix.distribution.ledger import read_records, write_all
from dealix.distribution.paths import DRAFTS_LEDGER
from dealix.distribution.schemas import validate_record

_ARABIC_RE = re.compile(r"[؀-ۿ]")
_URL_RE = re.compile(r"https?://", re.IGNORECASE)
_CTA_RE = re.compile(r"(CTA[:：]|call to action)", re.IGNORECASE)

MIN_LEN = 60
MAX_LEN = 2000
KNOWN_STATUSES = {STATUS_PENDING, STATUS_APPROVED, STATUS_REJECTED, STATUS_COPIED}


def check_draft(draft: dict[str, Any]) -> dict[str, Any]:
    """Return ``{id, passed, errors, warnings}`` for one draft."""
    errors: list[str] = []
    warnings: list[str] = []
    body = str(draft.get("body") or "")

    banned = scan_text_for_banned_claims(body)
    if banned:
        errors.append(f"banned_claim_phrases:{banned}")

    if draft.get("policy") != OPERATING_MODE:
        errors.append(f"policy_must_be_{OPERATING_MODE}")

    if draft.get("status") not in KNOWN_STATUSES:
        errors.append(f"unknown_status:{draft.get('status')!r}")

    lvl = draft.get("evidence_level", 0)
    if not isinstance(lvl, int) or isinstance(lvl, bool) or not (0 <= lvl <= 5):
        errors.append(f"invalid_evidence_level:{lvl!r}")

    if not _CTA_RE.search(body) and "؟" not in body:
        errors.append("missing_cta")

    if not _ARABIC_RE.search(body):
        errors.append("missing_arabic_body")

    n = len(body.strip())
    if n < MIN_LEN:
        errors.append(f"too_short:{n}<{MIN_LEN}")
    elif n > MAX_LEN:
        errors.append(f"too_long:{n}>{MAX_LEN}")

    schema_errs = validate_record(draft, "draft")
    if schema_errs:
        errors.append(f"schema:{schema_errs}")

    if body.count("؟") > 3:
        warnings.append("too_many_asks")
    if _URL_RE.search(body):
        warnings.append("contains_raw_url")

    return {
        "id": draft.get("id"),
        "prospect_id": draft.get("prospect_id"),
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
    }


def run_quality_gate(
    drafts: list[dict[str, Any]] | None = None,
    *,
    ledger: Path | None = None,
    persist: bool = False,
) -> dict[str, Any]:
    """Run the gate over all drafts (or a supplied list)."""
    led = ledger or DRAFTS_LEDGER
    records = drafts if drafts is not None else read_records(led)
    results = [check_draft(d) for d in records]
    failed = [r for r in results if not r["passed"]]

    if persist and drafts is None:
        by_id = {r["id"]: r for r in results}
        for rec in records:
            res = by_id.get(rec.get("id"))
            if res:
                rec["quality"] = {"passed": res["passed"], "errors": res["errors"]}
        write_all(led, records)

    return {
        "total": len(results),
        "passed": len(results) - len(failed),
        "failed": len(failed),
        "ok": not failed,
        "results": results,
        "failures": failed,
    }


__all__ = ["MAX_LEN", "MIN_LEN", "check_draft", "run_quality_gate"]
