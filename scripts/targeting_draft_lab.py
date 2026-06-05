#!/usr/bin/env python3
"""Draft Lab — builds tailored outreach drafts. It NEVER sends.

Every draft is evidence-backed, names one CTA, makes no exaggerated promises, and
is stamped ``APPROVAL_REQUIRED: founder``. The Draft Lab is the line Dealix does
not cross automatically: drafts are queued for manual founder review and manual
send only.

Draft rules (enforced in code by ``validate_draft``):
    - company name present
    - a stated reason for targeting (positive signal)
    - a respectfully-phrased weakness / opportunity
    - exactly one CTA
    - no auto-send, no guarantees

Usage:
    python scripts/targeting_draft_lab.py \\
        --in data/targeting/company_master.jsonl \\
        --out data/targeting/out --limit 10
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from scripts.targeting_common import COMPANY_MASTER, OUT_DIR, load_companies
from scripts.targeting_offer_router import route_offer
from scripts.targeting_weakness_mapper import WEAKNESS_LABEL_AR

# Banned phrases — exaggerated promises we never put in a draft.
BANNED_PHRASES = [
    "مضمون",
    "نضمن",
    "guarantee",
    "guaranteed",
    "100%",
    "زيادة مؤكدة",
    "أرباح مضمونة",
    "نضاعف",
    "double your",
    "10x",
]

# Positive-signal phrasing in Arabic for the "reason for targeting" line.
POSITIVE_SIGNAL_AR = {
    "growth_signal": "توسّعكم الأخير",
    "hiring_signal": "توظيفكم النشط",
    "partnership_signal": "شراكتكم الأخيرة",
    "serves_many_clients": "قاعدة عملائكم الواسعة",
    "case_study_presence": "عرضكم لأعمالكم",
}

# Respectful weakness phrasing in Arabic (opportunity, not criticism).
WEAKNESS_OPPORTUNITY_AR = {
    "revenue_leakage": "تنظيم متابعة الفرص حتى لا تتسرّب",
    "proof_gap": "تحويل نتائجكم إلى سجلّ إثبات واضح",
    "command_fog": "توحيد القرار التنفيذي في لوحة واحدة",
    "delivery_blindness": "إظهار حالة التسليم لحظة بلحظة",
    "client_memory_gap": "بناء ذاكرة عميل لا تضيع مع الوقت",
    "support_recurrence": "تقليل تكرار مشاكل الدعم",
    "data_fragmentation": "جمع بياناتكم المتفرقة في مكان واحد",
    "governance_risk": "إطار حوكمة خفيف لاستخدام AI والبيانات",
    "partner_potential": "تشغيل أول حلقة شراكة لخدمة عملائكم",
}


def _positive_signal(company: dict[str, Any]) -> str:
    for field, phrase in POSITIVE_SIGNAL_AR.items():
        if company.get(field):
            return phrase
    services = company.get("services") or []
    if services:
        return f"تخصصكم في {services[0]}"
    return "حضوركم في السوق"


def build_draft(company: dict[str, Any], routed: dict[str, Any] | None = None) -> dict[str, Any]:
    """Compose a first-touch draft for a company. Returns a dict with markdown."""
    routed = routed or route_offer(company)
    name = company.get("company_name", "—")
    positive = _positive_signal(company)
    weakness = routed["primary_weakness"]
    weakness_ar = WEAKNESS_LABEL_AR.get(weakness, weakness)
    opportunity = WEAKNESS_OPPORTUNITY_AR.get(
        weakness, "تنظيم أول حلقة تشغيل حول الفرص والدليل والقرار"
    )
    offer = routed["offer"]
    includes = "\n".join(f"  - {x}" for x in offer["includes"])
    evidence = "، ".join(company.get("source_urls", []) or ["—"])

    body = f"""السلام عليكم [الاسم في {name}]،

راجعت حضور {name} بشكل سريع، وواضح أن عندكم {positive}.

الفرصة التي لاحظتها ليست "أداة AI" فقط، بل {opportunity} — أول operating loop حول: الفرص، المتابعة، الدليل، والقرار التنفيذي القادم.

أبني Dealix كنظام تشغيل أعمال AI للشركات السعودية. نبدأ عادة بـ {offer['name_ar']} يطلع:
{includes}

بدون إرسال تلقائي أو وعود مبالغ فيها — فقط تشخيص وتشغيل أولي قابل للمراجعة.

يناسبك أرسل لك Diagnostic مختصر؟"""

    markdown = f"""<!-- DRAFT — APPROVAL_REQUIRED: founder — DO NOT AUTO-SEND -->
### {name}

- **سبب الاستهداف / reason:** {positive}
- **نقطة الضعف / weakness:** {weakness_ar} → {routed['primary_os_angle']}
- **العرض المقترح / offer:** {offer['name_ar']} ({offer.get('price_sar', 0)} SAR)
- **القناة / channel:** {company.get('contact_channel', 'official')}
- **الدليل / evidence:** {evidence}
- **CTA:** يناسبك أرسل لك Diagnostic مختصر؟

```
{body}
```

**APPROVAL_REQUIRED:** founder · **AUTO_SEND:** false
"""
    draft = {
        "company_name": name,
        "offer_id": routed["offer_id"],
        "weakness": weakness,
        "cta": "يناسبك أرسل لك Diagnostic مختصر؟",
        "body": body,
        "markdown": markdown,
        "approval_required": "founder",
        "auto_send": False,
    }
    draft["validation"] = validate_draft(draft, company)
    return draft


def validate_draft(draft: dict[str, Any], company: dict[str, Any]) -> dict[str, Any]:
    """Enforce the draft rules. Returns {ok, issues}."""
    issues: list[str] = []
    body = draft.get("body", "")
    if not draft.get("company_name"):
        issues.append("missing_company_name")
    if not company.get("source_urls"):
        issues.append("missing_evidence")
    # exactly one CTA — we phrase the CTA as a single question.
    if body.count("؟") + body.count("?") != 1:
        issues.append("cta_must_be_single")
    low = body.lower()
    for phrase in BANNED_PHRASES:
        if phrase.lower() in low:
            issues.append(f"banned_phrase:{phrase}")
    if draft.get("auto_send"):
        issues.append("auto_send_must_be_false")
    if draft.get("approval_required") != "founder":
        issues.append("founder_approval_required")
    return {"ok": not issues, "issues": issues}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Dealix outreach Draft Lab (no auto-send)")
    ap.add_argument("--in", dest="infile", default=str(COMPANY_MASTER))
    ap.add_argument("--out", dest="outdir", default=str(OUT_DIR))
    ap.add_argument("--limit", type=int, default=10)
    args = ap.parse_args(argv)

    companies = load_companies(Path(args.infile))[: args.limit]
    drafts = [build_draft(c) for c in companies]
    out_dir = Path(args.outdir)
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "drafts_for_review.md"
    header = (
        "# Drafts for Review — APPROVAL REQUIRED (founder)\n\n"
        "> Dealix never auto-sends. Each draft below is a proposal for manual "
        "review and manual send.\n\n"
    )
    blocks = [d["markdown"] for d in drafts]
    path.write_text(header + "\n---\n".join(blocks), encoding="utf-8")

    invalid = [d["company_name"] for d in drafts if not d["validation"]["ok"]]
    print(f"drafts={len(drafts)} valid={len(drafts) - len(invalid)} out={path}")
    if invalid:
        print("NEEDS FIX:", ", ".join(invalid))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
