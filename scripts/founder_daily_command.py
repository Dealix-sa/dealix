#!/usr/bin/env python3
"""Founder Daily Command — one screen of "what do I do today".

Reads the growth + revenue ledgers and the private-launch readiness report,
then writes reports/founder/daily_command.md. Read-only over the ledgers;
it never sends or changes anything. Pure stdlib.

    python scripts/founder_daily_command.py
    cat reports/founder/daily_command.md
"""

from __future__ import annotations

import csv
import datetime as _dt
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = ROOT / "data" / "growth" / "first_30_targets.csv"
OUTREACH = ROOT / "data" / "revenue" / "outreach_queue.jsonl"
DIAGNOSTICS = ROOT / "data" / "revenue" / "diagnostics.jsonl"
OFFERS = ROOT / "data" / "revenue" / "offers.jsonl"
PAYMENTS = ROOT / "data" / "revenue" / "payments.jsonl"
UPSELLS = ROOT / "data" / "revenue" / "upsells.jsonl"
READINESS = ROOT / "reports" / "launch" / "private_launch_readiness.md"
OUT = ROOT / "reports" / "founder" / "daily_command.md"


def _rows(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def _jsonl(path: Path) -> list[dict]:
    out = []
    if not path.is_file():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def _readiness_score() -> tuple[int, str]:
    if not READINESS.is_file():
        return (0, "unknown (report missing)")
    text = READINESS.read_text(encoding="utf-8")
    m = re.search(r"[Ss]core[^0-9]*(\d{1,3})\s*/\s*100", text)
    score = int(m.group(1)) if m else 0
    if score >= 85:
        verdict = "Public Limited Ready"
    elif score >= 70:
        verdict = "Private Launch Ready"
    elif score >= 50:
        verdict = "Internal Only"
    else:
        verdict = "No-Go"
    return (score, verdict)


def main() -> int:
    targets = _rows(TARGETS)
    outreach = _jsonl(OUTREACH)
    diagnostics = _jsonl(DIAGNOSTICS)
    offers = _jsonl(OFFERS)
    payments = _jsonl(PAYMENTS)
    upsells = _jsonl(UPSELLS)
    score, verdict = _readiness_score()

    by_status: dict[str, list[dict]] = {}
    for t in targets:
        by_status.setdefault((t.get("status") or "research").strip(), []).append(t)

    approved_drafts = [o for o in outreach if o.get("approval_status") == "approved"]
    pending_drafts = [o for o in outreach if o.get("approval_status") in ("draft", None, "")]

    today = _dt.date.today().isoformat()
    lines: list[str] = []
    add = lines.append

    add(f"# Founder Daily Command — {today}")
    add("")
    add(f"**Private launch readiness:** {score}/100 ({verdict})")
    add("")

    add("## 1. Today's top 5 founder actions")
    actions: list[str] = []
    if score < 70:
        actions.append(
            "Raise launch readiness to >= 70 (run scripts/verify_dealix_launch_readiness.py)."
        )
    if pending_drafts:
        actions.append(f"Review {len(pending_drafts)} outreach draft(s) in the approval queue.")
    research = by_status.get("research", [])
    if research:
        actions.append(
            f"Qualify {min(5, len(research))} of {len(research)} research targets (add evidence/warm intro)."
        )
    if approved_drafts:
        actions.append(f"Send {len(approved_drafts)} approved message(s) manually.")
    if by_status.get("diagnostic_booked"):
        actions.append(f"Run {len(by_status['diagnostic_booked'])} booked diagnostic(s).")
    if by_status.get("offer_sent"):
        actions.append(f"Follow up on {len(by_status['offer_sent'])} sent offer(s).")
    if not actions:
        actions.append("Pick 5 targets, qualify them, draft outreach for founder approval.")
    for a in actions[:5]:
        add(f"- {a}")
    add("")

    add("## 2. Outreach due")
    if approved_drafts:
        for o in approved_drafts:
            add(f"- SEND: {o.get('company','?')} — approved, send manually")
    else:
        add("- No approved messages waiting. (Approve drafts first — nothing auto-sends.)")
    if pending_drafts:
        add(f"- {len(pending_drafts)} draft(s) awaiting your review.")
    add("")

    add("## 3. Diagnostics due")
    booked = by_status.get("diagnostic_booked", [])
    if booked or diagnostics:
        for t in booked:
            add(f"- {t.get('company_name','?')} — run diagnostic, write 02_diagnostic_summary.md")
        for d in diagnostics:
            if d.get("status") not in ("done", "complete", "completed"):
                add(f"- {d.get('company','?')} — diagnostic logged ({d.get('status','open')})")
    else:
        add("- None booked yet.")
    add("")

    add("## 4. Offers pending")
    sent_offers = by_status.get("offer_sent", [])
    if sent_offers or offers:
        for t in sent_offers:
            add(f"- {t.get('company_name','?')} — offer sent, follow up")
        for o in offers:
            add(f"- {o.get('company','?')} — offer logged ({o.get('status','?')})")
    else:
        add("- None.")
    add("")

    add("## 5. Active deliveries")
    paid = by_status.get("paid", [])
    if paid or payments:
        for t in paid:
            add(f"- {t.get('company_name','?')} — PAID, deliver Command Sprint")
        for p in payments:
            add(f"- {p.get('company','?')} — payment confirmed {p.get('date','')}")
    else:
        add("- No active paid deliveries yet.")
    add("")

    add("## 6. Proof packs due")
    if paid:
        for t in paid:
            add(f"- {t.get('company_name','?')} — assemble 10_proof_pack.md by day 7")
    else:
        add("- None due (no paid sprint in delivery).")
    add("")

    add("## 7. Upsell opportunities")
    if upsells:
        for u in upsells:
            add(f"- {u.get('company','?')} — {u.get('recommended_offer','review')}")
    else:
        add("- None yet. Upsell only after a delivered Proof Pack.")
    add("")

    add("## 8. Blockers")
    blockers = []
    if score < 70:
        blockers.append("Readiness below private-launch threshold (70).")
    if not targets:
        blockers.append("No targets in first_30_targets.csv.")
    if not outreach:
        blockers.append("No outreach drafts queued.")
    if blockers:
        for b in blockers:
            add(f"- {b}")
    else:
        add("- None blocking. Execute the daily loop.")
    add("")

    add("## 9. Stop doing")
    add("- No cold outreach, no scraping, no auto-send.")
    add("- No guaranteed-revenue language in any message.")
    add("- No expansion (dashboards/SaaS/ads/sector pages) before 3 paid Sprints + 3 Proof Packs.")
    add("")

    add("## 10. Private launch verdict")
    if score >= 70:
        add(f"- **GO** for private launch ({score}/100). Send up to 5 approved messages manually.")
    else:
        add(f"- **NO-GO** ({score}/100). Close readiness gaps first.")
    add("")
    add("---")
    add("_Generated by scripts/founder_daily_command.py — read-only, never sends._")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} (readiness {score}/100, {verdict})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
