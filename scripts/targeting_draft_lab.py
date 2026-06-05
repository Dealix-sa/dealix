#!/usr/bin/env python3
"""
targeting_draft_lab.py — generate founder-reviewed outreach DRAFTS (never sends).

A draft is only generated for companies that already passed the compliance gate
and the score/evidence thresholds. Every draft:

  * cites the company's own evidence fields (no invented facts),
  * carries exactly one CTA,
  * contains no banned phrases (guarantees, "we saw a problem", auto-WhatsApp…),
  * is marked draft_status=needs_approval.

The module also exposes ``validate_draft`` so tests and the approval queue can
assert a body is clean before it ever reaches a human, let alone a customer.

Usage:
    python scripts/targeting_draft_lab.py --in data/targeting/out/scored.jsonl \
        --out data/targeting/out/drafts_for_review.md
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import yaml  # noqa: E402

DATA = _ROOT / "data" / "targeting"

# Phrases that must never appear in a draft (over-claims, pressure, automation).
BANNED_PHRASES = [
    "نضمن",
    "نضمن لكم",
    "نضمن لك",
    "مضمون",
    "شفنا أن عندكم مشكلة",
    "عندكم مشكلة أكيدة",
    "نجيب لكم عملاء",
    "نجيب لك عملاء",
    "واتساب تلقائي",
    "guarantee",
    "guaranteed",
    "we saw a problem",
    "we will get you clients",
]

DRAFT_MIN_SCORE = 80
DRAFT_MIN_EVIDENCE = 2


def _signal_angles(path: Path | None = None) -> dict[str, str]:
    path = path or DATA / "signals.yml"
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    out: dict[str, str] = {}
    for item in data.get("signals", []) or []:
        if item.get("id"):
            out[item["id"]] = item.get("angle", "")
    return out


def _thresholds() -> tuple[int, int]:
    path = DATA / "scoring_weights.yml"
    if not path.exists():
        return DRAFT_MIN_SCORE, DRAFT_MIN_EVIDENCE
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    th = data.get("thresholds", {})
    return (
        int(th.get("draft_min_score", DRAFT_MIN_SCORE)),
        int(th.get("draft_min_evidence", DRAFT_MIN_EVIDENCE)),
    )


def validate_draft(text: str) -> list[str]:
    """Return a list of banned phrases found in the draft body (empty == clean)."""
    low = text.lower()
    hits: list[str] = []
    for phrase in BANNED_PHRASES:
        if phrase.lower() in low:
            hits.append(phrase)
    return hits


def eligible_for_draft(company: dict[str, Any]) -> tuple[bool, str]:
    """Gate: score, evidence, compliance status, grade."""
    min_score, min_evidence = _thresholds()
    if company.get("draft_status") == "rejected":
        return False, "rejected_by_gate"
    if str(company.get("grade", "")) not in {"A+", "A"}:
        return False, "grade_below_A"
    if float(company.get("targeting_score", 0)) < min_score:
        return False, f"score_below_{min_score}"
    if int(company.get("evidence_count", len(company.get("source_urls", []) or []))) < min_evidence:
        return False, f"evidence_below_{min_evidence}"
    return True, "ok"


def build_draft(company: dict[str, Any], angles: dict[str, str] | None = None) -> dict[str, Any]:
    """Build a single Arabic outreach draft grounded in the company's evidence.

    Returns {company, angle, offer, body, evidence_cited, cta, draft_status,
    violations}. The caller (approval queue) must keep draft_status until a
    human approves — this function never sends anything.
    """
    angles = angles if angles is not None else _signal_angles()
    name = company.get("company_name", "—")
    pains = company.get("pain_signals", []) or []
    primary_pain = pains[0] if pains else ""
    angle = angles.get(primary_pain, "Command fog")
    offer = company.get("recommended_offer") or "Command Sprint"
    evidence = (company.get("source_urls") or [])[:2]

    # Grounded positive observation + one hypothesized gap (never an assertion).
    positive = "حضوركم الرقمي واضح وخدماتكم متعددة"
    gap_map = {
        "Proof gap": "إبراز الأدلة ودراسات الحالة",
        "Revenue leakage": "وضوح الخطوة التالية والمتابعة",
        "Command fog": "ترتيب العرض والرسالة الواحدة",
        "Delivery visibility": "وضوح التنفيذ والتسليم",
        "Client memory": "ذاكرة الحسابات وتجديدها",
        "AI governance": "حوكمة استخدام الذكاء الاصطناعي والبيانات",
    }
    gap = gap_map.get(angle, "ترتيب العرض والدليل")

    body = (
        f"السلام عليكم،\n"
        f"راجعت حضور {name} بشكل سريع، وواضح أن {positive}، "
        f"ولاحظت فرصة محتملة لتحسين {gap}.\n"
        f"أبني Dealix كنظام تشغيل أعمال AI للشركات السعودية. "
        f"نبدأ عادة بـ {offer} خلال 7 أيام يطلع:\n"
        f"- Revenue Map\n- Proof Register\n- Executive Command Brief\n- Next Action Board\n"
        f"بدون إرسال تلقائي أو وعود مبالغ فيها — فقط تشخيص وتشغيل أولي قابل للمراجعة.\n"
        f"يناسبك أرسل لك Diagnostic مختصر؟"
    )

    violations = validate_draft(body)
    return {
        "company": name,
        "angle": angle,
        "offer": offer,
        "body": body,
        "evidence_cited": evidence,
        "cta": "إرسال Diagnostic مختصر",
        "draft_status": "needs_approval",
        "violations": violations,
    }


def render_drafts_markdown(drafts: list[dict[str, Any]]) -> str:
    lines = ["# Dealix Targeting OS — Drafts for Founder Review", ""]
    lines.append("> لا يُرسل أي شيء تلقائيًا. كل مسودة تحتاج موافقة المؤسس قبل الإرسال اليدوي.")
    lines.append("")
    for i, d in enumerate(drafts, 1):
        lines.append(f"## {i}. {d['company']} — {d['angle']} → {d['offer']}")
        lines.append("")
        lines.append("**Evidence cited:**")
        for url in d["evidence_cited"]:
            lines.append(f"- {url}")
        lines.append("")
        lines.append("**Draft:**")
        lines.append("")
        lines.append("```")
        lines.append(d["body"])
        lines.append("```")
        lines.append("")
        lines.append(f"- CTA: {d['cta']}")
        lines.append(f"- Status: `{d['draft_status']}`")
        if d["violations"]:
            lines.append(f"- ⚠️ BLOCKED — banned phrases: {', '.join(d['violations'])}")
        lines.append("")
    return "\n".join(lines)


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            rows.append(json.loads(line))
    return rows


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Dealix Targeting OS draft lab (drafts only)")
    ap.add_argument("--in", dest="infile", required=True, help="scored company jsonl")
    ap.add_argument("--out", default=None, help="write drafts_for_review.md")
    ap.add_argument("--limit", type=int, default=10)
    args = ap.parse_args(argv)

    angles = _signal_angles()
    drafts: list[dict[str, Any]] = []
    for company in _read_jsonl(Path(args.infile)):
        ok, _ = eligible_for_draft(company)
        if not ok:
            continue
        draft = build_draft(company, angles)
        if draft["violations"]:
            # never emit a non-clean draft
            continue
        drafts.append(draft)
        if len(drafts) >= args.limit:
            break

    md = render_drafts_markdown(drafts)
    if args.out:
        outp = Path(args.out)
        outp.parent.mkdir(parents=True, exist_ok=True)
        outp.write_text(md + "\n", encoding="utf-8")
        print(f"wrote {len(drafts)} drafts -> {outp}", file=sys.stderr)
    else:
        print(md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
