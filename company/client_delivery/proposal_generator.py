#!/usr/bin/env python3
"""
Client Delivery — Proposal Generator

Generates a tailored proposal in Arabic for a client based on their
diagnostic results. Output: company/runtime/clients/{slug}/proposals/

Usage:
    python company/client_delivery/proposal_generator.py \
        --client <slug> \
        --package diagnostic_sprint \
        --price 12500 \
        --pilot-price 7500 \
        --timeline "14 يومًا"
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLIENTS_DIR = ROOT / "company" / "runtime" / "clients"

PACKAGE_LABELS = {
    "free_diagnostic": "تشخيص مجاني",
    "micro_sprint": "Micro Sprint",
    "data_pack": "Data Pack",
    "managed_ops": "Managed Ops",
    "diagnostic_sprint": "Transformation Diagnostic Sprint",
    "enterprise": "Enterprise System",
}


def generate_proposal(
    slug: str,
    package: str,
    price_sar: float,
    pilot_price_sar: float = 0,
    timeline: str = "14 يومًا",
    retainer_price_sar: float = 0,
) -> dict:
    intake_path = CLIENTS_DIR / slug / "intake.json"
    if not intake_path.exists():
        raise FileNotFoundError(f"Client not found: {slug}")
    intake = json.loads(intake_path.read_text())

    diag_path = CLIENTS_DIR / slug / "diagnostic" / "diagnostic.json"
    diagnostic = json.loads(diag_path.read_text()) if diag_path.exists() else {}

    today = date.today()
    valid_until = today + timedelta(days=30)

    prop_num = f"PROP-{today.year}-{today.strftime('%m%d')}"

    proposal = {
        "proposal_number": prop_num,
        "client_slug": slug,
        "company_name": intake["company_name"],
        "contact_name": intake["contact_name"],
        "package": package,
        "package_label": PACKAGE_LABELS.get(package, package),
        "price_sar": price_sar,
        "pilot_price_sar": pilot_price_sar,
        "retainer_price_sar": retainer_price_sar,
        "timeline": timeline,
        "issue_date": today.isoformat(),
        "valid_until": valid_until.isoformat(),
        "diagnostic_summary": diagnostic.get("metrics", {}),
        "recommendation": diagnostic.get("recommendation", ""),
        "top_priorities": diagnostic.get("top_priorities", []),
    }

    out_dir = CLIENTS_DIR / slug / "proposals"
    out_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{prop_num}.json"
    (out_dir / filename).write_text(json.dumps(proposal, ensure_ascii=False, indent=2))

    md = _render_proposal(proposal)
    (out_dir / f"{prop_num}.md").write_text(md)

    return proposal


def _render_proposal(p: dict) -> str:
    m = p.get("diagnostic_summary", {})
    priorities = p.get("top_priorities", [])
    priorities_text = "\n".join(f"{i+1}. {pr}" for i, pr in enumerate(priorities)) if priorities else "— حسب نتائج التشخيص"

    leakage = m.get("leakage_estimate_sar", 0)
    leakage_str = f"{leakage:,.0f} SAR/شهر" if leakage else "حسب التشخيص"

    pilot_section = ""
    if p["pilot_price_sar"]:
        pilot_section = f"""
### خيار B: التشخيص + Pilot 7 أيام (موصى به)

```
التشخيص ({p['package_label']})     {p['price_sar']:,.0f} SAR
Pilot Build (7 أيام)              {p['pilot_price_sar']:,.0f} SAR
──────────────────────────────────────────────
المجموع                          {p['price_sar'] + p['pilot_price_sar']:,.0f} SAR
```
"""

    retainer_section = ""
    if p["retainer_price_sar"]:
        retainer_section = f"""
### خيار C: التشخيص + Pilot + Retainer أول 3 أشهر

```
التشخيص + Pilot                  {p['price_sar'] + p['pilot_price_sar']:,.0f} SAR
Retainer × 3 أشهر               {p['retainer_price_sar'] * 3:,.0f} SAR
──────────────────────────────────────────────
المجموع                          {p['price_sar'] + p['pilot_price_sar'] + p['retainer_price_sar'] * 3:,.0f} SAR
```
"""

    return f"""# عرض أسعار — {p['company_name']}

| البند | التفاصيل |
|-------|----------|
| رقم العرض | {p['proposal_number']} |
| تاريخ الإصدار | {p['issue_date']} |
| صالح حتى | {p['valid_until']} |
| مُعدّ لـ | {p['company_name']} — {p['contact_name']} |
| مُعدّ من | سامي الحربي، Dealix |

---

## 1. ملخص التشخيص

بناءً على تحليلنا لعمليات {p['company_name']}، رصدنا تسربًا تقديريًا في الإيراد
يبلغ **{leakage_str}**.

### الأولويات الثلاث للإصلاح

{priorities_text}

### التوصية المبدئية

{p.get('recommendation', 'حسب نتائج التشخيص')}

---

## 2. الحل المقترح

**الباقة المقترحة**: {p['package_label']}
**الجدول الزمني**: {p['timeline']}

---

## 3. الأسعار

### خيار A: {p['package_label']} فقط

```
{p['package_label']}               {p['price_sar']:,.0f} SAR
──────────────────────────────────────────────
المجموع                           {p['price_sar']:,.0f} SAR
```
{pilot_section}{retainer_section}

---

## 4. شروط الدفع

| الدفعة | المبلغ | الموعد |
|--------|--------|--------|
| الأولى (للبداية) | 50% | قبل يوم البداية |
| الثانية | 50% | عند تسليم المخرجات |

طرق الدفع: تحويل بنكي، STC Pay، Mada.

---

## 5. ضمانات العمل

- ✅ لا تغيير دون موافقتكم
- ✅ لا إرسال تلقائي لأي رسائل
- ✅ يمكن الإيقاف في أي وقت
- ✅ سرية تامة للبيانات
- ✅ نتائج قابلة للقياس

---

## 6. الخطوة التالية

1. ردوا باختياركم (A / B / C)
2. نرسل عقد الخدمة (صفحة واحدة)
3. بعد التوقيع، نرسل رابط الدفع
4. نبدأ خلال 48 ساعة

---

*هذا العرض سري ومعدّ خصيصًا لـ {p['company_name']}. صالح حتى {p['valid_until']}.*
*Dealix | سامي الحربي | sami.assiri11@gmail.com*
"""


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate client proposal")
    p.add_argument("--client", required=True)
    p.add_argument("--package", required=True, choices=sorted(PACKAGE_LABELS.keys()))
    p.add_argument("--price", type=float, required=True)
    p.add_argument("--pilot-price", type=float, default=0)
    p.add_argument("--retainer-price", type=float, default=0)
    p.add_argument("--timeline", default="14 يومًا")
    return p.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    try:
        result = generate_proposal(
            slug=args.client,
            package=args.package,
            price_sar=args.price,
            pilot_price_sar=args.pilot_price,
            retainer_price_sar=args.retainer_price,
            timeline=args.timeline,
        )
        print(f"PROPOSAL_OK | {result['proposal_number']} | {result['company_name']}")
        print(f"Files: company/runtime/clients/{result['client_slug']}/proposals/")
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
