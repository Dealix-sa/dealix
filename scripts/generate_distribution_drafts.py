#!/usr/bin/env python3
"""Product Distribution OS — approval-first draft generator.

Turns qualified prospects into *internal* outreach drafts. Every draft:

  - is marked ``approval_required=True`` and ``status="pending_approval"``
    (or ``needs_edit`` when a guard trips) — never a "sent" state;
  - is evidence level ``L1`` (internal draft, not customer-ready) per
    ``auto_client_acquisition.proof_engine.evidence.EvidenceLevel``;
  - is run through the existing doctrine guards before it is written:
      * ``governance_os.policy_check_draft``  — forbidden channels / claims
      * ``data_os.pii_flags_for_row``         — log/PII hygiene
      * ``safe_send_gateway.enforce_doctrine_non_negotiables`` — posture

This script NEVER sends anything (no email / WhatsApp / LinkedIn) and never
scrapes. It only reads a local prospect file and appends draft rows for a
human to review. See docs/distribution/PRODUCT_DISTRIBUTION_OS_AR.md.

Run:
    python scripts/generate_distribution_drafts.py
"""

from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from auto_client_acquisition.data_os import pii_flags_for_row
from auto_client_acquisition.governance_os import policy_check_draft
from auto_client_acquisition.safe_send_gateway import enforce_doctrine_non_negotiables

ROOT = Path(__file__).resolve().parents[1]
PROSPECTS = ROOT / "data" / "distribution" / "prospects.json"
PROSPECTS_EXAMPLE = ROOT / "data" / "distribution" / "prospects.example.json"
DRAFTS = ROOT / "data" / "drafts" / "drafts.jsonl"
REPORT = ROOT / "reports" / "distribution" / "DRAFT_GENERATION_REPORT.md"

# Prospects in these states are eligible for a first-touch draft.
ELIGIBLE_STATES = {"new", "qualified"}

# Content-level PII patterns (belt-and-suspenders on top of pii_flags_for_row,
# which is column-name driven). We never want a contact email/phone baked into
# a draft body — drafts reference role + company + sector, not personal data.
_EMAIL_IN_TEXT = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")
_PHONE_IN_TEXT = re.compile(r"(?<!\w)\+?\d[\d\s\-]{8,}\d(?!\w)")


def now_iso() -> str:
    """ISO-8601 UTC timestamp."""
    return datetime.now(UTC).isoformat()


def load_prospects(path: Path | None = None) -> list[dict[str, Any]]:
    """Load prospects from the local file, falling back to the example file.

    No network, no scraping — local JSON only.
    """
    target = path or PROSPECTS
    if not target.exists():
        target = PROSPECTS_EXAMPLE
    if not target.exists():
        return []
    data = json.loads(target.read_text(encoding="utf-8"))
    return data if isinstance(data, list) else data.get("prospects", [])


def build_first_message_ar(prospect: dict[str, Any]) -> str:
    """Render the Arabic first-touch outreach body.

    Intentionally references role/company/sector/pain only — no PII, no
    guaranteed-result claims, no channel-automation language.
    """
    company = prospect.get("company", "شركتكم")
    sector = prospect.get("sector", "الشركات")
    pain = prospect.get("pain_hypothesis", "ضياع فرص المتابعة وتشتّت العمليات اليومية")
    return (
        f"السلام عليكم،\n\n"
        f"ألاحظ أن كثيرًا من {sector} عندهم فرص واستفسارات حقيقية، لكن جزءًا منها يضيع "
        f"بسبب {pain}.\n\n"
        f"في Dealix نبني نظام عمليات إيرادات يساعد {company} على ترتيب المتابعة، توضيح "
        "الأولويات، وتحويل العمل اليومي إلى فرص قابلة للقياس — بدون أتمتة إرسال عشوائي.\n\n"
        "إذا كان مناسبًا، أرسل لكم تشخيصًا مختصرًا يوضّح أين قد تكون الفرص الضائعة، "
        "وكيف نبدأ بأول workflow عملي. لا وعود بنتائج مضمونة — نبدأ بإثبات صغير قابل للقياس."
    )


def _content_pii_issues(text: str) -> list[str]:
    """Return PII issue codes found directly in draft text."""
    issues: list[str] = []
    if _EMAIL_IN_TEXT.search(text):
        issues.append("pii_email_in_body")
    if _PHONE_IN_TEXT.search(text):
        issues.append("pii_phone_in_body")
    return issues


def draft_guard_issues(draft: dict[str, Any]) -> list[str]:
    """Run a draft through the existing doctrine guards; return issue codes.

    Empty list ⇒ safe to queue as ``pending_approval``.
    Non-empty  ⇒ caller must set status ``needs_edit``.
    """
    issues: list[str] = []

    # 1) Forbidden channel / claim language (reuses the governed pre-check).
    text = f"{draft.get('subject', '')}\n{draft.get('body', '')}"
    verdict = policy_check_draft(text)
    if not verdict.allowed:
        issues.extend(verdict.issues)

    # 2) Column-name PII heuristic over the persisted row.
    issues.extend(f"pii_{flag.reason}" for flag in pii_flags_for_row(draft))

    # 3) Content-level PII in the body text itself.
    issues.extend(_content_pii_issues(text))

    return list(dict.fromkeys(issues))


def build_draft(prospect: dict[str, Any]) -> dict[str, Any]:
    """Build a single approval-first draft for a prospect.

    Always returns a draft with ``approval_required=True`` and a status of
    ``pending_approval`` (clean) or ``needs_edit`` (a guard tripped). It never
    returns a "sent" state.
    """
    timestamp = now_iso()
    draft: dict[str, Any] = {
        "id": f"draft_{uuid4().hex[:12]}",
        "prospect_id": str(prospect.get("id", "")),
        "company": prospect.get("company", ""),
        "sector": prospect.get("sector", ""),
        "channel": prospect.get("preferred_channel", "email"),
        "draft_type": "outreach_first",
        "language": "ar",
        "subject": "تشخيص فرص المتابعة والعمليات",
        "body": build_first_message_ar(prospect),
        "offer_angle": prospect.get("offer_angle", "AI Revenue Operations diagnostic"),
        "evidence_level": "L1",  # internal draft — not customer-ready
        "risk_level": "low",
        "approval_required": True,
        "status": "pending_approval",
        "policy_issues": [],
        "created_at": timestamp,
        "updated_at": timestamp,
        "next_action": "Founder approval before any manual send",
    }

    issues = draft_guard_issues(draft)
    if issues:
        draft["status"] = "needs_edit"
        draft["policy_issues"] = issues
        draft["next_action"] = "Fix before approval: " + ", ".join(issues)
    return draft


def generate_drafts(prospects: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Pure transform: eligible prospects → approval-first drafts (no I/O)."""
    return [build_draft(p) for p in prospects if str(p.get("status", "new")) in ELIGIBLE_STATES]


def write_drafts(drafts: list[dict[str, Any]], path: Path = DRAFTS) -> None:
    """Append drafts to the append-only JSONL ledger."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        for draft in drafts:
            fh.write(json.dumps(draft, ensure_ascii=False) + "\n")


def render_report(scanned: int, drafts: list[dict[str, Any]]) -> str:
    """Render the markdown generation report."""
    pending = [d for d in drafts if d["status"] == "pending_approval"]
    needs_edit = [d for d in drafts if d["status"] == "needs_edit"]
    lines = [
        "# Draft Generation Report",
        "",
        f"Generated: {now_iso()}",
        f"Prospects scanned: {scanned}",
        f"Drafts created: {len(drafts)}",
        f"Pending approval: {len(pending)}",
        f"Needs edit (guard tripped): {len(needs_edit)}",
        "",
        "## Safety posture",
        "- No external send performed (email / WhatsApp / LinkedIn).",
        "- No scraping. Prospects read from a local file only.",
        "- Every draft is L1 (internal draft) and requires founder approval.",
        "",
        "## Next action",
        "- Review pending drafts in reports/distribution/DRAFT_QUEUE_REVIEW.md",
        "- Resolve any `needs_edit` drafts before approval.",
    ]
    if needs_edit:
        lines.append("")
        lines.append("## Needs edit")
        for draft in needs_edit[:50]:
            lines.append(
                f"- `{draft['id']}` — {draft.get('company')} — "
                f"{', '.join(draft.get('policy_issues', []))}"
            )
    return "\n".join(lines) + "\n"


def main() -> None:
    # Assert the operating posture is doctrine-clean before doing any work.
    # Raises ValueError if a forbidden action were ever requested.
    enforce_doctrine_non_negotiables()

    prospects = load_prospects()
    drafts = generate_drafts(prospects)
    write_drafts(drafts)

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(render_report(len(prospects), drafts), encoding="utf-8")

    pending = sum(1 for d in drafts if d["status"] == "pending_approval")
    print(f"DEALIX_DRAFT_GENERATION_CREATED={len(drafts)}")
    print(f"DEALIX_DRAFT_GENERATION_PENDING={pending}")


if __name__ == "__main__":
    main()
