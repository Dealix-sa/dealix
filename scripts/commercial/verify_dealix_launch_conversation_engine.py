#!/usr/bin/env python3
"""Verify the Dealix Launch Conversation & Negotiation Engine outputs.

Checks (all must pass):
  - canonical founder email present, no other founder email leaked
  - data files present
  - reports + CSVs generated
  - approval queue exists and every external action requires approval
  - email + whatsapp drafts + negotiation playbooks generated
  - no live-send / cold-WhatsApp / fake-guarantee language
  - every message carries a CTA
  - proof packs invent no results

Exit 0 = PASS, non-zero = FAIL.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.conversation_engine import company_brain  # noqa: E402
from dealix.conversation_engine.company_brain import CANONICAL_FOUNDER_EMAIL  # noqa: E402

DATA_DIR = ROOT / "data" / "dealix_conversation_negotiation"
REPORT_DIR = ROOT / "reports" / "dealix_conversation_negotiation"

DATA_FILES = [
    "founder_profile.json", "offers.json", "personas.json", "objections.json",
    "channels.json", "proof_rules.json", "seed_targets.json",
]
REPORT_FILES = [
    "latest.json", "latest.md", "approval_queue.csv", "opportunity_graph.csv",
    "email_drafts.csv", "whatsapp_drafts.csv", "negotiation_playbooks.csv", "proof_pack.md",
    "slack_brief.md",
]

# Any other founder-looking email would be a leak. Add known-bad here if found.
FORBIDDEN_EMAIL_FRAGMENTS: list[str] = []

FAKE_GUARANTEE_MARKERS = [
    "guaranteed revenue", "guaranteed roi", "نضمن زيادة", "مضمون النتائج",
    "government access", "guaranteed contracts",
]

# Arabic negations that flip a "guarantee" marker into an anti-guarantee promise
# ("we do NOT guarantee"). Such negated usage is allowed and must not be flagged.
_NEGATIONS = ("ما ", "لا ", "بدون ", "غير ", "don't", "do not", "never")


def _affirmative_marker_present(marker: str, blob: str) -> bool:
    """True only if `marker` appears WITHOUT a preceding negation."""
    start = 0
    while True:
        idx = blob.find(marker, start)
        if idx == -1:
            return False
        window = blob[max(0, idx - 12):idx]
        if not any(neg in window for neg in _NEGATIONS):
            return True
        start = idx + len(marker)


def _fail(failures: list[str], msg: str) -> None:
    failures.append(msg)


def main() -> int:
    failures: list[str] = []

    # 1. canonical founder email
    profile = company_brain.founder_profile()
    if profile.get("canonical_email") != CANONICAL_FOUNDER_EMAIL:
        _fail(failures, "founder canonical_email is not the approved address")

    # 2. data files present
    for name in DATA_FILES:
        if not (DATA_DIR / name).is_file():
            _fail(failures, f"missing data file: {name}")

    # 3. report files present (run the engine first if missing)
    missing_reports = [n for n in REPORT_FILES if not (REPORT_DIR / n).is_file()]
    if missing_reports:
        _fail(failures, f"missing report files (run the engine first): {missing_reports}")
        _summarize(failures)
        return 1 if failures else 0

    payload = json.loads((REPORT_DIR / "latest.json").read_text(encoding="utf-8"))

    # 4. no other founder email leaked anywhere in the payload
    blob = json.dumps(payload, ensure_ascii=False).lower()
    if CANONICAL_FOUNDER_EMAIL not in blob:
        _fail(failures, "canonical founder email not present in report payload")
    for frag in FORBIDDEN_EMAIL_FRAGMENTS:
        if frag.lower() in blob:
            _fail(failures, f"forbidden founder email fragment leaked: {frag}")

    # 5. no live send
    if payload.get("summary", {}).get("live_send") is not False:
        _fail(failures, "summary.live_send must be False")
    if payload.get("verdict") != "SAFE_TO_RUN_INTERNAL_DRAFT_ONLY":
        _fail(failures, f"unexpected verdict: {payload.get('verdict')}")

    # 6. approval queue present and every external action requires approval
    approvals = payload.get("approval_queue", [])
    if not approvals:
        _fail(failures, "approval_queue is empty")
    for a in approvals:
        if not a.get("approval_required"):
            _fail(failures, f"approval item {a.get('id')} does not require approval")
        if a.get("status") != "pending_founder_approval":
            _fail(failures, f"approval item {a.get('id')} not pending_founder_approval")

    # 7. drafts + playbooks generated
    if not payload.get("email_drafts"):
        _fail(failures, "no email drafts generated")
    if not payload.get("whatsapp_drafts"):
        _fail(failures, "no whatsapp drafts generated")
    if not payload.get("negotiation_playbooks"):
        _fail(failures, "no negotiation playbooks generated")

    # 8. CTA present in every email + whatsapp draft
    for d in payload.get("email_drafts", []):
        if not str(d.get("cta", "")).strip():
            _fail(failures, f"email draft for {d.get('company')} missing CTA")
    for d in payload.get("whatsapp_drafts", []):
        if not str(d.get("permission_cta", "")).strip():
            _fail(failures, f"whatsapp draft for {d.get('company')} missing CTA")
        if not d.get("cold_send_forbidden"):
            _fail(failures, f"whatsapp draft for {d.get('company')} missing cold_send_forbidden guard")

    # 9. no fake guarantees anywhere (negated "we do NOT guarantee" is allowed)
    for marker in FAKE_GUARANTEE_MARKERS:
        if _affirmative_marker_present(marker.lower(), blob):
            _fail(failures, f"fake-guarantee language detected: {marker}")

    # 10. proof packs invent no results
    for pack in payload.get("proof_packs", []):
        if pack.get("safe") is False or pack.get("violations"):
            _fail(failures, f"proof pack for {pack.get('company')} contains forbidden claims")

    _summarize(failures)
    return 1 if failures else 0


def _summarize(failures: list[str]) -> None:
    print("DEALIX_LAUNCH_CONVERSATION_ENGINE_VERIFY=" + ("PASS" if not failures else "FAIL"))
    print(f"canonical_founder_email={CANONICAL_FOUNDER_EMAIL}")
    if failures:
        for f in failures:
            print("FAIL: " + f)
    else:
        print("all checks passed (draft-only, approval-first, no fake claims)")


if __name__ == "__main__":
    raise SystemExit(main())
