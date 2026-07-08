"""Money Now Sprint — first-revenue engine (draft-only, evidence-based).

Generates a founder action plan for closing the 499 SAR Revenue Proof Sprint:
today's top offer, up to 10 target prospects, draft messages, a manual payment
checklist, evidence-event checklist, and proof-pack delivery checklist.

Revenue is only recognized when a `payment_received` evidence event exists.
Nothing is sent. Nothing is charged.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

from .schemas import EVIDENCE_CHAIN, REVENUE_RECOGNITION_EVENT

ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT / "reports" / "money_now"
DATA_DIR = ROOT / "data" / "money_now"
EVIDENCE_PATH = DATA_DIR / "evidence_events.json"

TOP_OFFER = {
    "name": "Revenue Proof Sprint",
    "price_sar": 499,
    "promise": "A fast, honest proof that Dealix can find and close a revenue leak.",
    "closeability": "high — low price, clear scope, manual delivery.",
}


@dataclass
class EvidenceEvent:
    prospect: str
    event: str
    detail: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"prospect": self.prospect, "event": self.event, "detail": self.detail}


@dataclass
class MoneyNowPlan:
    run_date: date
    top_offer: dict[str, Any]
    prospects: list[str]
    draft_messages: dict[str, str]
    payment_checklist: list[str]
    evidence_checklist: list[str]
    proof_pack_checklist: list[str]
    follow_up_queue: list[str]
    recognized_revenue_sar: int = 0
    outputs: dict[str, str] = field(default_factory=dict)


def load_evidence_events(path: Path | None = None) -> list[EvidenceEvent]:
    p = path or EVIDENCE_PATH
    if not p.exists():
        return []
    try:
        raw = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    events = raw.get("events", raw) if isinstance(raw, dict) else raw
    result: list[EvidenceEvent] = []
    for item in events or []:
        if not isinstance(item, dict):
            continue
        result.append(
            EvidenceEvent(
                prospect=str(item.get("prospect", "")),
                event=str(item.get("event", "")),
                detail=str(item.get("detail", "")),
            )
        )
    return result


def recognized_revenue(events: list[EvidenceEvent]) -> int:
    """Sum of 499 SAR per prospect that has a payment_received event. Revenue is
    never recognized without that event."""

    paid = {
        e.prospect
        for e in events
        if e.event == REVENUE_RECOGNITION_EVENT and e.prospect
    }
    return len(paid) * TOP_OFFER["price_sar"]


def _draft_message(prospect: str) -> str:
    return (
        f"مرحباً {prospect}،\n"
        "لاحظنا أن أغلب شركات B2B في السوق السعودي تفقد إيرادات بسبب ضعف المتابعة، "
        "وليس بسبب نقص العملاء.\n"
        "نقترح Revenue Proof Sprint بـ 499 ريال: نحلل تسريب إيراد واحد ونعطيك خطة "
        "إغلاق قابلة للتطبيق خلال أيام.\n"
        "الهدف هو إثبات القيمة أولاً، ثم نقيس النتيجة معاً.\n"
        "— مسودة للمراجعة قبل الإرسال —"
    )


def build_plan(
    prospects: list[str] | None = None, run_date: date | None = None
) -> MoneyNowPlan:
    run_date = run_date or date.today()
    prospects = (prospects or _default_prospect_slots())[:10]

    draft_messages = {p: _draft_message(p) for p in prospects}
    events = load_evidence_events()

    return MoneyNowPlan(
        run_date=run_date,
        top_offer=dict(TOP_OFFER),
        prospects=prospects,
        draft_messages=draft_messages,
        payment_checklist=[
            "Confirm scope of the 499 SAR Revenue Proof Sprint in writing (draft).",
            "Prepare a manual invoice draft (do NOT auto-issue).",
            "Share manual payment link/details only after founder approval.",
            "Record payment_received evidence event once payment is confirmed.",
            "No live charge is enabled; all payment steps are manual.",
        ],
        evidence_checklist=[f"[ ] {e}" for e in EVIDENCE_CHAIN],
        proof_pack_checklist=[
            "Diagnose the specific revenue leak.",
            "Record target list, drafts, approvals, and manual sends.",
            "Capture replies, calls, invoice status, payment status.",
            "Summarize delivered work and before/after (real data only).",
            "Mark any missing evidence as MISSING — never fabricate.",
            "Deliver proof pack; record proof_pack_delivered event.",
        ],
        follow_up_queue=[
            f"Follow up with {p} (manual, after prior message approved)."
            for p in prospects
        ],
        recognized_revenue_sar=recognized_revenue(events),
    )


def _default_prospect_slots() -> list[str]:
    """Placeholder slots — the founder fills in real warm-list names. No fake
    customers are invented; these are empty labeled slots."""

    return [f"Prospect Slot {i}" for i in range(1, 11)]


def write_plan(plan: MoneyNowPlan) -> dict[str, str]:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    d = plan.run_date.isoformat()

    # Seed an evidence-events file schema if none exists (empty, safe).
    if not EVIDENCE_PATH.exists():
        EVIDENCE_PATH.write_text(
            json.dumps(
                {
                    "schema": "dealix.money_now.evidence_events.v1",
                    "note": "Revenue recognized only when a payment_received event exists.",
                    "allowed_events": list(EVIDENCE_CHAIN),
                    "events": [],
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    json_path = REPORTS_DIR / f"{d}_money_now.json"
    md_path = REPORTS_DIR / f"{d}_money_now.md"

    json_path.write_text(
        json.dumps(
            {
                "date": d,
                "mode": "draft-only",
                "top_offer": plan.top_offer,
                "prospects": plan.prospects,
                "draft_messages": plan.draft_messages,
                "payment_checklist": plan.payment_checklist,
                "evidence_checklist": plan.evidence_checklist,
                "proof_pack_checklist": plan.proof_pack_checklist,
                "follow_up_queue": plan.follow_up_queue,
                "recognized_revenue_sar": plan.recognized_revenue_sar,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    md_path.write_text(_render_md(plan), encoding="utf-8")

    plan.outputs = {
        "json": str(json_path.relative_to(ROOT)),
        "md": str(md_path.relative_to(ROOT)),
        "evidence": str(EVIDENCE_PATH.relative_to(ROOT)),
    }
    return plan.outputs


def _render_md(plan: MoneyNowPlan) -> str:
    d = plan.run_date.isoformat()
    o = plan.top_offer
    lines = [
        f"# Money Now Sprint — Founder Action Plan {d}",
        "",
        "> Draft-only. No message is sent. No charge is taken. Revenue is only "
        "counted when a `payment_received` event exists.",
        "",
        "## Today's top closeable offer",
        f"- **{o['name']}** — {o['price_sar']} SAR",
        f"- Promise: {o['promise']}",
        f"- Closeability: {o['closeability']}",
        "",
        f"## Recognized revenue so far: {plan.recognized_revenue_sar} SAR",
        "",
        "## Target prospects (max 10 — fill in real warm-list names)",
    ]
    lines += [f"- {p}" for p in plan.prospects]
    lines += ["", "## Manual payment checklist"]
    lines += [f"- {c}" for c in plan.payment_checklist]
    lines += ["", "## Evidence-event checklist"]
    lines += [f"- {c}" for c in plan.evidence_checklist]
    lines += ["", "## Proof-pack delivery checklist"]
    lines += [f"- {c}" for c in plan.proof_pack_checklist]
    lines += ["", "## Follow-up queue (manual)"]
    lines += [f"- {c}" for c in plan.follow_up_queue]
    lines += [
        "",
        "## Draft messages (review before any send)",
    ]
    for p, msg in plan.draft_messages.items():
        lines += [f"### {p}", "", "```", msg, "```", ""]
    return "\n".join(lines) + "\n"
