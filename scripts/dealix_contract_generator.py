#!/usr/bin/env python3
"""
Dealix Service Contract Generator
===================================
Generates a bilingual AR+EN service agreement after a deal is won.
The founder reviews and sends — nothing auto-sends.

Usage:
  python3 scripts/dealix_contract_generator.py \
    --company "شركة نجم اللوجستية" \
    --contact "أحمد العتيبي" \
    --sector logistics \
    --tier revenue_os \
    --start-date 2026-07-01

  python3 scripts/dealix_contract_generator.py --list-tiers

Doctrine: generates draft only. Founder signs and sends. No auto-send.
"""

from __future__ import annotations

import argparse
import json
import uuid
from datetime import date, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PITCHES_FILE = REPO_ROOT / "data/outreach/sector_pitches.json"
OUTPUT_DIR = REPO_ROOT / "reports/contracts"

TIERS = {
    "sprint": {
        "label_ar": "باقة التشخيص السريع",
        "label_en": "Revenue Intelligence Sprint",
        "setup_sar": 499,
        "monthly_sar": 0,
        "duration_months": 0,
        "deliverables_ar": "تشخيص 30 نقطة + تقرير فجوات + خارطة طريق 90 يوم",
        "deliverables_en": "30-point diagnostic + gap report + 90-day roadmap",
        "payment_terms_ar": "دفعة واحدة عند البدء",
        "payment_terms_en": "Single payment upon kickoff",
    },
    "revenue_os": {
        "label_ar": "نظام تشغيل الإيرادات",
        "label_en": "Revenue OS",
        "setup_sar": 18_000,
        "monthly_sar": 5_000,
        "duration_months": 3,
        "deliverables_ar": (
            "إعداد نظام الذكاء التجاري + تكامل WhatsApp/CRM + "
            "لوحة قيادة الإيرادات + تدريب الفريق + دعم شهري"
        ),
        "deliverables_en": (
            "Commercial intelligence setup + WhatsApp/CRM integration + "
            "revenue dashboard + team training + monthly support"
        ),
        "payment_terms_ar": "18,000 ريال إعداد + 5,000 ريال/شهر لمدة 3 أشهر",
        "payment_terms_en": "18,000 SAR setup + 5,000 SAR/month for 3 months",
    },
    "command_center": {
        "label_ar": "مركز القيادة الذكي",
        "label_en": "Command Center OS",
        "setup_sar": 35_000,
        "monthly_sar": 9_000,
        "duration_months": 6,
        "deliverables_ar": (
            "جميع مكونات Revenue OS + "
            "ذكاء السوق المتقدم + تقارير إدارية أسبوعية + "
            "مدير حساب مخصص + SLA 4 ساعات"
        ),
        "deliverables_en": (
            "All Revenue OS components + "
            "advanced market intelligence + weekly executive reports + "
            "dedicated account manager + 4-hour SLA"
        ),
        "payment_terms_ar": "35,000 ريال إعداد + 9,000 ريال/شهر لمدة 6 أشهر",
        "payment_terms_en": "35,000 SAR setup + 9,000 SAR/month for 6 months",
    },
    "delivery_os": {
        "label_ar": "نظام تشغيل التسليم",
        "label_en": "Delivery OS",
        "setup_sar": 25_000,
        "monthly_sar": 6_000,
        "duration_months": 3,
        "deliverables_ar": (
            "تحسين عمليات التسليم + تتبع SLA + "
            "إشعارات العملاء الآلية + لوحة قيادة العمليات"
        ),
        "deliverables_en": (
            "Delivery operations optimization + SLA tracking + "
            "automated customer notifications + operations dashboard"
        ),
        "payment_terms_ar": "25,000 ريال إعداد + 6,000 ريال/شهر لمدة 3 أشهر",
        "payment_terms_en": "25,000 SAR setup + 6,000 SAR/month for 3 months",
    },
    "review_os": {
        "label_ar": "نظام المراجعة والسمعة",
        "label_en": "Review & Reputation OS",
        "setup_sar": 12_000,
        "monthly_sar": 3_500,
        "duration_months": 3,
        "deliverables_ar": (
            "نظام جمع المراجعات + ردود ذكية على Google + "
            "تقرير سمعة شهري + تنبيهات فورية"
        ),
        "deliverables_en": (
            "Review collection system + smart Google responses + "
            "monthly reputation report + instant alerts"
        ),
        "payment_terms_ar": "12,000 ريال إعداد + 3,500 ريال/شهر لمدة 3 أشهر",
        "payment_terms_en": "12,000 SAR setup + 3,500 SAR/month for 3 months",
    },
}

CONTRACT_TEMPLATE = """\
# عقد خدمات Dealix | Dealix Services Agreement
# {contract_id}
# للمراجعة الداخلية فقط — يتطلب توقيع الفاوندر قبل الإرسال

---

**رقم العقد / Contract ID**: {contract_id}
**تاريخ الإصدار / Issue Date**: {issue_date}
**صالح حتى / Valid Until**: {expiry_date}

---

## الأطراف | Parties

| | الطرف الأول / Party A | الطرف الثاني / Party B |
|--|--|--|
| **الاسم** | Dealix (شركة ديلكس للتقنية) | {company_name} |
| **المسؤول** | سامي العسيري — المؤسس | {contact_name} |
| **البريد** | hello@dealix.me | — |
| **الموقع** | dealix.me | — |

---

## الخدمة المتفق عليها | Agreed Service

**الباقة / Package**: {tier_label_ar} ({tier_label_en})

**القطاع / Sector**: {sector_ar} / {sector_en}

**تاريخ البدء / Start Date**: {start_date}

**مدة العقد / Duration**: {duration_str}

---

## المستحقات | Deliverables

### بالعربي:
{deliverables_ar}

### English:
{deliverables_en}

---

## شروط الدفع | Payment Terms

### بالعربي:
{payment_terms_ar}

**إجمالي العقد**: {total_sar} ريال سعودي

### English:
{payment_terms_en}

**Contract Total**: {total_sar} SAR

> **ملاحظة**: الدفع عبر Moyasar — رابط الدفع يُرسل بعد توقيع العقد.
> **Note**: Payment via Moyasar — payment link sent after contract signature.

---

## شروط الخدمة | Service Terms

### الالتزامات | Commitments

**Dealix تلتزم بـ / Dealix commits to:**
- تسليم المستحقات في المواعيد المحددة
- دعم فني مستمر طوال مدة العقد
- تقارير دورية عن الأداء والنتائج
- سرية تامة لبيانات العميل (PDPL + NCA)

*Dealix commits to: on-time delivery, continuous technical support, periodic performance reports, and full data confidentiality (PDPL + NCA).*

**العميل يلتزم بـ / Client commits to:**
- توفير وصول المعلومات والأنظمة اللازمة للتكامل
- تسمية مسؤول تقني داخلي للتنسيق
- الالتزام بمواعيد الدفع المتفق عليها
- عدم مشاركة المستحقات مع أطراف ثالثة

*Client commits to: providing system access, naming an internal technical contact, meeting payment timelines, and not sharing deliverables with third parties.*

### السرية | Confidentiality

جميع المعلومات المتبادلة بين الطرفين تُعدّ سرية ولا يجوز الإفصاح عنها لأطراف ثالثة دون موافقة خطية مسبقة.

*All information exchanged between the parties is confidential and may not be disclosed to third parties without prior written consent.*

### الإنهاء | Termination

- يحق لأي طرف إنهاء العقد بإشعار 30 يوم خطي
- المبالغ المدفوعة عن فترة الخدمة المنجزة غير قابلة للاسترداد
- يحق للعميل استرداد رسوم الشهر الجاري إذا لم تُسلَّم المستحقات الأساسية

*Either party may terminate with 30 days written notice. Fees for completed service periods are non-refundable. The client may reclaim the current month's fee if core deliverables have not been delivered.*

---

## التوقيعات | Signatures

| | Dealix | {company_name} |
|--|--|--|
| **الاسم / Name** | سامي العسيري | {contact_name} |
| **التوقيع / Signature** | __________________ | __________________ |
| **التاريخ / Date** | __________________ | __________________ |

---

*Dealix — نظام التشغيل الذكي للشركات السعودية B2B*
*hello@dealix.me | dealix.me | الرياض*

---

> **⚠️ للمؤسس**: هذا مسودة داخلية للمراجعة. لا ترسله للعميل قبل مراجعة قانونية.
> راجع الشروط، حدّث بيانات العميل، ثم احصل على توقيع إلكتروني (e.g. DocuSign).
"""


def _load_pitches() -> dict:
    if not PITCHES_FILE.exists():
        return {}
    with PITCHES_FILE.open(encoding="utf-8") as f:
        return json.load(f)


def _contract_id() -> str:
    return f"DLX-{date.today().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"


def generate_contract(
    company: str,
    contact: str,
    sector: str,
    tier: str,
    start_date: date | None = None,
    dry_run: bool = False,
) -> Path | None:
    if tier not in TIERS:
        print(f"[ERROR] Unknown tier: {tier}. Use --list-tiers.")
        return None

    pitches = _load_pitches()
    sectors = pitches.get("sectors", {})
    if sector not in sectors:
        print(f"[ERROR] Unknown sector: {sector}")
        return None

    sector_data = sectors[sector]
    tier_data = TIERS[tier]
    start = start_date or (date.today() + timedelta(days=7))
    contract_id = _contract_id()
    issue_date = date.today().isoformat()
    expiry_date = (date.today() + timedelta(days=14)).isoformat()

    duration_months = tier_data["duration_months"]
    if duration_months == 0:
        duration_str = "مرة واحدة / One-time"
        total_sar = tier_data["setup_sar"]
    else:
        duration_str = f"{duration_months} أشهر / {duration_months} months"
        total_sar = tier_data["setup_sar"] + (tier_data["monthly_sar"] * duration_months)

    contract = CONTRACT_TEMPLATE.format(
        contract_id=contract_id,
        issue_date=issue_date,
        expiry_date=expiry_date,
        company_name=company,
        contact_name=contact,
        tier_label_ar=tier_data["label_ar"],
        tier_label_en=tier_data["label_en"],
        sector_ar=sector_data["label_ar"],
        sector_en=sector_data["label_en"],
        start_date=start.isoformat(),
        duration_str=duration_str,
        deliverables_ar=tier_data["deliverables_ar"],
        deliverables_en=tier_data["deliverables_en"],
        payment_terms_ar=tier_data["payment_terms_ar"],
        payment_terms_en=tier_data["payment_terms_en"],
        total_sar=f"{total_sar:,}",
    )

    if dry_run:
        print(contract[:3000] + ("\n...[truncated]" if len(contract) > 3000 else ""))
        return None

    out_dir = OUTPUT_DIR / date.today().strftime("%Y-%m-%d")
    out_dir.mkdir(parents=True, exist_ok=True)
    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in company)
    out_file = out_dir / f"contract_{safe_name}_{tier}_{contract_id}.md"
    out_file.write_text(contract, encoding="utf-8")

    print()
    print("━" * 65)
    print("📄 SERVICE CONTRACT GENERATED — FOUNDER REVIEW REQUIRED")
    print("━" * 65)
    print(f"  Contract ID : {contract_id}")
    print(f"  Company     : {company}")
    print(f"  Contact     : {contact}")
    print(f"  Tier        : {tier_data['label_ar']} ({tier_data['label_en']})")
    print(f"  Sector      : {sector_data['label_ar']} ({sector_data['label_en']})")
    print(f"  Start Date  : {start.isoformat()}")
    print(f"  Valid Until : {expiry_date}")
    print(f"  Total Value : {total_sar:,} SAR")
    print(f"  File        : {out_file}")
    print()
    print("  NEXT STEPS:")
    print("  [ ] Review all terms and update contact details")
    print("  [ ] Get legal review before sending (optional but recommended)")
    print("  [ ] Send via DocuSign or PDF — never paste raw markdown")
    print(f"  [ ] After signing: make invoice AMOUNT={tier_data['setup_sar']}")
    print("  [ ] Update outreach_log.csv: make outreach-tracker update \\")
    print(f"      --company '{company}' --status won")
    print("━" * 65)
    print()

    return out_file


def list_tiers() -> None:
    print("\nAvailable tiers:")
    print(f"  {'Key':<20} {'Setup (SAR)':<14} {'Monthly (SAR)':<16} {'Label'}")
    print(f"  {'---':<20} {'-----------':<14} {'-------------':<16} {'-----'}")
    for key, t in TIERS.items():
        monthly = f"{t['monthly_sar']:,}/mo" if t["monthly_sar"] else "—"
        print(f"  {key:<20} {t['setup_sar']:>10,}    {monthly:<16} {t['label_en']}")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate bilingual service contract (founder review required)"
    )
    parser.add_argument("--company", help="Company name")
    parser.add_argument("--contact", help="Contact name", default="المسؤول")
    parser.add_argument("--sector", help="Sector key")
    parser.add_argument("--tier", help="Service tier key", choices=list(TIERS))
    parser.add_argument("--start-date", help="Service start date (YYYY-MM-DD)")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing file")
    parser.add_argument("--list-tiers", action="store_true", help="List available tiers")
    args = parser.parse_args()

    if args.list_tiers:
        list_tiers()
        return

    if not args.company or not args.sector or not args.tier:
        parser.error("--company, --sector, and --tier are required")

    start_date = None
    if args.start_date:
        from datetime import datetime
        start_date = datetime.strptime(args.start_date, "%Y-%m-%d").date()

    generate_contract(
        company=args.company,
        contact=args.contact,
        sector=args.sector,
        tier=args.tier,
        start_date=start_date,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
