#!/usr/bin/env python3
"""GTM Quality + Compliance Gate (CI doctrine check).

Fast, fail-closed check that the Market Production OS honors its hard
rules. Exits non-zero if ANY of these hold:

  - the factory produces a non-draft send_status
  - a clean draft is wrongly blocked
  - a known-bad draft (cold whatsapp / guaranteed claim / scraping source /
    missing unsubscribe / sub-P1 personalization / fake Re: subject) is
    wrongly allowed
  - MAX_AUTO_SENDS != 0

Optionally validate an external drafts file with ``--drafts path.jsonl``:
every record must include unsubscribe and pass the gate.

Usage:
  python3 scripts/gtm_quality_gate.py
  python3 scripts/gtm_quality_gate.py --drafts data/market_production_os/drafts.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from auto_client_acquisition.market_production_os import (  # noqa: E402
    MAX_AUTO_SENDS,
    Prospect,
    check_draft,
    produce_drafts,
    summarize_batch,
)
from auto_client_acquisition.market_production_os.schemas import (  # noqa: E402
    PersonalizationLevel,
    SendStatus,
)

_CLEAN_BODY = (
    "مرحبًا، لاحظنا نمطًا في القطاع يتعلق بضعف متابعة العملاء المحتملين. "
    "نقترح تشخيصًا محدود النطاق. هذه فرص مُثبتة بأدلة. لإيقاف الرسائل ردّ بكلمة إيقاف."
)

# (label, kwargs, expect_pass)
_P2 = int(PersonalizationLevel.P2)
_P0 = int(PersonalizationLevel.P0)
_CASES = [
    ("clean_draft", {"subject": "ملاحظة سريعة", "body": _CLEAN_BODY,
                     "personalization_level": _P2, "evidence_level": 2,
                     "unsubscribe_included": True}, True),
    ("cold_whatsapp", {"subject": "hi", "body": "Use cold whatsapp to reach everyone",
                       "personalization_level": _P2, "evidence_level": 2,
                       "unsubscribe_included": True}, False),
    ("guaranteed_claim", {"subject": "offer", "body": "We guarantee ROI in 30 days",
                          "personalization_level": _P2, "evidence_level": 2,
                          "unsubscribe_included": True}, False),
    ("scraping_source", {"subject": "ملاحظة", "body": _CLEAN_BODY,
                         "personalization_level": _P2, "evidence_level": 2,
                         "unsubscribe_included": True, "lead_source": "scraping"}, False),
    ("missing_unsubscribe", {"subject": "ملاحظة", "body": _CLEAN_BODY,
                             "personalization_level": _P2, "evidence_level": 2,
                             "unsubscribe_included": False}, False),
    ("below_p1", {"subject": "ملاحظة", "body": _CLEAN_BODY,
                  "personalization_level": _P0, "evidence_level": 2,
                  "unsubscribe_included": True}, False),
    ("fake_thread", {"subject": "Re: our deal", "body": _CLEAN_BODY,
                     "personalization_level": _P2, "evidence_level": 2,
                     "unsubscribe_included": True}, False),
]


def _check_cases() -> list[str]:
    failures: list[str] = []
    for label, kwargs, expect_pass in _CASES:
        result = check_draft(**kwargs)
        if result.passed != expect_pass:
            failures.append(
                f"case {label}: expected pass={expect_pass}, got {result.passed} "
                f"reasons={result.reasons}"
            )
    return failures


def _check_factory() -> list[str]:
    failures: list[str] = []
    if MAX_AUTO_SENDS != 0:
        failures.append(f"MAX_AUTO_SENDS must be 0, got {MAX_AUTO_SENDS}")
    drafts = produce_drafts(
        [Prospect(prospect_id="p1", company="شركة", sector="clinics")],
        offers=["Free AI Ops Diagnostic"],
        target=25,
    )
    if any(d.send_status != SendStatus.DRAFT.value for d in drafts):
        failures.append("factory produced a non-draft send_status")
    if summarize_batch(drafts)["auto_sent"] != 0:
        failures.append("factory reported auto_sent != 0")
    return failures


def _check_drafts_file(path: Path) -> list[str]:
    failures: list[str] = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        row = json.loads(line)
        if not row.get("unsubscribe_included", False):
            failures.append(f"{path.name}:{i} missing unsubscribe")
        result = check_draft(
            subject=str(row.get("subject", "")),
            body=str(row.get("body", "")),
            personalization_level=int(row.get("personalization_level", 0)),
            evidence_level=int(row.get("evidence_level", 0)),
            unsubscribe_included=bool(row.get("unsubscribe_included", False)),
            recipient_email=str(row.get("recipient_email", "")),
            lead_source=str(row.get("source", "founder_supplied")),
        )
        if not result.passed:
            failures.append(f"{path.name}:{i} blocked: {result.reasons}")
        if row.get("send_status", "draft") == "sent":
            failures.append(f"{path.name}:{i} send_status=sent (auto-send forbidden)")
    return failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="GTM quality + compliance gate.")
    parser.add_argument("--drafts", type=Path, default=None)
    args = parser.parse_args(argv)

    failures = _check_cases() + _check_factory()
    if args.drafts and args.drafts.exists():
        failures += _check_drafts_file(args.drafts)

    if failures:
        print("GTM_QUALITY_GATE=FAIL")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("GTM_QUALITY_GATE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
