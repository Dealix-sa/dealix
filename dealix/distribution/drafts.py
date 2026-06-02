"""Draft Factory — per-sector first-touch / follow-up message drafts.

Every draft is ``draft_pending_approval`` and carries
``policy = draft_only_no_auto_send``. The factory:

  - loads a per-sector AR template (falls back to ``_default_ar.md``);
  - fills ``{company}`` / ``{pain}`` placeholders;
  - runs the canonical doctrine guard + banned-phrase scan BEFORE writing;
  - de-dupes (one open draft per prospect) so re-runs are idempotent.

It NEVER sends anything. ``approve`` / ``reject`` / ``mark_copied`` are explicit
human transitions.
"""

from __future__ import annotations

from functools import cache, lru_cache
from pathlib import Path
from typing import Any

from dealix.distribution import sectors as sectors_mod
from dealix.distribution.doctrine import (
    OPERATING_MODE,
    STATUS_APPROVED,
    STATUS_COPIED,
    STATUS_PENDING,
    STATUS_REJECTED,
    assert_distribution_safe,
    scan_text_for_banned_claims,
)
from dealix.distribution.ledger import (
    append_record,
    new_id,
    now_iso,
    read_records,
    update_status,
)
from dealix.distribution.paths import DRAFTS_LEDGER, TEMPLATES_DIR
from dealix.distribution.prospects import load_prospects

_OPEN_STATUSES = {STATUS_PENDING, STATUS_APPROVED, STATUS_COPIED}


@cache
def _load_template(sector_key: str) -> str:
    path = TEMPLATES_DIR / f"{sector_key}_ar.md"
    if not path.is_file():
        path = TEMPLATES_DIR / "_default_ar.md"
    return (
        path.read_text(encoding="utf-8")
        if path.is_file()
        else (
            "السلام عليكم {company}،\n\n{pain}\n\n"
            "CTA: هل يناسبكم تشخيص مختصر (Risk Score)؟\n\n"
            "— Dealix (مسودة — موافقة قبل أي إرسال)\n"
        )
    )


def build_draft(
    prospect: dict[str, Any], *, sector_info: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Build a single draft dict for a prospect (does not write it)."""
    # Fail-fast: a draft is never a cold/bulk/automated send.
    assert_distribution_safe()

    sector_key = str(prospect.get("sector") or "")
    info = sector_info or sectors_mod.get_sector(sector_key) or {}
    company = str(prospect.get("company") or "فريقكم").strip()
    pain = str(prospect.get("pain_hypothesis") or info.get("pain") or "").strip()

    template = _load_template(sector_key)
    body = template.format(company=company, pain=pain).strip()

    banned = scan_text_for_banned_claims(body)
    if banned:
        raise ValueError(f"draft contains banned claim phrase(s): {banned}")

    channel = str(prospect.get("channel") or "email")
    return {
        "id": new_id("draft"),
        "prospect_id": str(prospect.get("id") or ""),
        "company": company,
        "sector": sector_key,
        "channel": channel,
        "language": "ar",
        "body": body,
        "evidence_level": 0,
        "policy": OPERATING_MODE,
        "status": STATUS_PENDING,
        "created_at": now_iso(),
    }


def _open_prospect_ids(existing: list[dict[str, Any]]) -> set[str]:
    return {str(d.get("prospect_id")) for d in existing if d.get("status") in _OPEN_STATUSES}


def generate_drafts(
    prospects: list[dict[str, Any]],
    *,
    existing: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Build drafts for prospects that don't already have an open draft."""
    existing = existing or []
    skip = _open_prospect_ids(existing)
    out: list[dict[str, Any]] = []
    index = {s["key"]: s for s in sectors_mod.load_sectors()}
    for pr in prospects:
        pid = str(pr.get("id") or "")
        if pid and pid in skip:
            continue
        out.append(build_draft(pr, sector_info=index.get(str(pr.get("sector") or ""))))
    return out


def run_generation(
    prospects_path: Path | None = None, *, ledger: Path | None = None
) -> dict[str, Any]:
    """Load prospects, generate missing drafts, append to the ledger."""
    led = ledger or DRAFTS_LEDGER
    prospects = load_prospects(prospects_path)
    existing = read_records(led)
    new_drafts = generate_drafts(prospects, existing=existing)
    for d in new_drafts:
        append_record(led, d)
    return {
        "prospects": len(prospects),
        "existing_drafts": len(existing),
        "new_drafts": len(new_drafts),
        "ids": [d["id"] for d in new_drafts],
        "policy": OPERATING_MODE,
    }


def all_drafts(ledger: Path | None = None) -> list[dict[str, Any]]:
    return read_records(ledger or DRAFTS_LEDGER)


def pending_drafts(ledger: Path | None = None) -> list[dict[str, Any]]:
    return [d for d in all_drafts(ledger) if d.get("status") == STATUS_PENDING]


def approve_draft(draft_id: str, ledger: Path | None = None) -> dict[str, Any] | None:
    return update_status(ledger or DRAFTS_LEDGER, draft_id, STATUS_APPROVED)


def reject_draft(
    draft_id: str, reason: str = "", ledger: Path | None = None
) -> dict[str, Any] | None:
    return update_status(ledger or DRAFTS_LEDGER, draft_id, STATUS_REJECTED, reject_reason=reason)


def mark_copied(draft_id: str, ledger: Path | None = None) -> dict[str, Any] | None:
    """Founder copied the (approved) draft for a manual send — still no auto-send."""
    return update_status(ledger or DRAFTS_LEDGER, draft_id, STATUS_COPIED)


__all__ = [
    "all_drafts",
    "approve_draft",
    "build_draft",
    "generate_drafts",
    "mark_copied",
    "pending_drafts",
    "reject_draft",
    "run_generation",
]
