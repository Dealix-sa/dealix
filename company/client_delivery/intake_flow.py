#!/usr/bin/env python3
"""
Client Delivery — Intake Flow

Processes a new client after contract signing:
- Creates client folder under company/runtime/clients/{slug}/
- Writes intake record JSON
- Generates intake checklist
- Validates required fields before starting diagnostic

Usage:
    python company/client_delivery/intake_flow.py \
        --name "شركة الأفق" \
        --sector "logistics" \
        --contact "أحمد العتيبي" \
        --phone "+966501234567" \
        --email "ahmed@ufq.sa" \
        --package "diagnostic_sprint" \
        --weekly-leads 80
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLIENTS_DIR = ROOT / "company" / "runtime" / "clients"

VALID_SECTORS = {
    "healthcare", "training", "restaurant", "real_estate",
    "logistics", "retail", "technology", "construction",
    "consulting", "education", "finance", "other",
}

VALID_PACKAGES = {
    "free_diagnostic", "micro_sprint", "data_pack",
    "managed_ops", "diagnostic_sprint", "enterprise",
}


def _slugify(name: str) -> str:
    slug = re.sub(r"[^\w\s-]", "", name, flags=re.UNICODE).strip()
    slug = re.sub(r"[\s_-]+", "-", slug)
    return slug.lower()[:40]


def create_client(
    name: str,
    sector: str,
    contact: str,
    phone: str,
    email: str,
    package: str,
    weekly_leads: int = 0,
    notes: str = "",
) -> dict:
    if sector not in VALID_SECTORS:
        raise ValueError(f"Unknown sector: {sector}. Valid: {sorted(VALID_SECTORS)}")
    if package not in VALID_PACKAGES:
        raise ValueError(f"Unknown package: {package}. Valid: {sorted(VALID_PACKAGES)}")

    slug = _slugify(name)
    client_dir = CLIENTS_DIR / slug
    client_dir.mkdir(parents=True, exist_ok=True)

    intake = {
        "client_slug": slug,
        "company_name": name,
        "sector": sector,
        "contact_name": contact,
        "contact_phone": phone,
        "contact_email": email,
        "package": package,
        "weekly_leads": weekly_leads,
        "notes": notes,
        "intake_date": date.today().isoformat(),
        "status": "active",
        "diagnostic_start": None,
        "diagnostic_end": None,
        "pilot_start": None,
        "pilot_end": None,
        "retainer_start": None,
    }

    intake_path = client_dir / "intake.json"
    intake_path.write_text(json.dumps(intake, ensure_ascii=False, indent=2))

    checklist = _generate_checklist(intake)
    (client_dir / "intake_checklist.md").write_text(checklist)

    return intake


def _generate_checklist(intake: dict) -> str:
    today = date.today().isoformat()
    return f"""# قائمة مراجعة الاستقبال — {intake['company_name']}

**التاريخ**: {today}
**الباقة**: {intake['package']}
**المسؤول**: {intake['contact_name']} ({intake['contact_phone']})

---

## قبل بداية التشخيص

- [ ] تم استلام الدفعة الأولى
- [ ] تم توقيع عقد الخدمة
- [ ] تم إرسال بريد تأكيد البداية
- [ ] تم تحديد موعد لقاء البداية (Kickoff)

## لقاء البداية (Kickoff)

- [ ] شرح منهجية التشخيص
- [ ] تحديد الأهداف القابلة للقياس
- [ ] طلب الوصول للأدوات المطلوبة (قراءة فقط)
- [ ] الاتفاق على جدول التسليم

## البيانات والوصول المطلوب

- [ ] قائمة العملاء المحتملين (CSV أو Excel)
- [ ] وصول WhatsApp Business (إن وُجد)
- [ ] وصول CRM أو نظام المتابعة الحالي
- [ ] بيانات المبيعات آخر 90 يومًا

## خلال التشخيص

- [ ] تحليل مسار الاستفسارات
- [ ] رصد نقاط التسرب
- [ ] مقابلة مع أحد أفراد فريق المبيعات
- [ ] حساب معدلات التحويل الحالية

## المخرجات للتسليم

- [ ] خريطة تسرب الإيراد
- [ ] الأولويات الثلاث
- [ ] توصية النظام المناسب
- [ ] خطة Pilot (إن شملتها الباقة)
- [ ] عرض أسعار المرحلة التالية

---

*أُنشئت تلقائيًا بواسطة نظام الاستقبال — Dealix*
"""


def load_client(slug: str) -> dict | None:
    path = CLIENTS_DIR / slug / "intake.json"
    if not path.exists():
        return None
    return json.loads(path.read_text())


def list_clients() -> list[dict]:
    clients = []
    for intake_file in CLIENTS_DIR.glob("*/intake.json"):
        try:
            clients.append(json.loads(intake_file.read_text()))
        except Exception:
            pass
    return sorted(clients, key=lambda c: c.get("intake_date", ""), reverse=True)


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Dealix client intake flow")
    p.add_argument("--name", required=True, help="Company name")
    p.add_argument("--sector", required=True, choices=sorted(VALID_SECTORS))
    p.add_argument("--contact", required=True, help="Contact person name")
    p.add_argument("--phone", required=True, help="Contact phone")
    p.add_argument("--email", required=True, help="Contact email")
    p.add_argument("--package", required=True, choices=sorted(VALID_PACKAGES))
    p.add_argument("--weekly-leads", type=int, default=0)
    p.add_argument("--notes", default="")
    p.add_argument("--list", action="store_true", help="List all clients")
    return p.parse_args()


if __name__ == "__main__":
    args = _parse_args()

    if args.list:
        clients = list_clients()
        if not clients:
            print("No clients found.")
        else:
            for c in clients:
                print(f"  {c['client_slug']:30s} | {c['company_name']:30s} | {c['package']:20s} | {c['status']}")
        sys.exit(0)

    try:
        intake = create_client(
            name=args.name,
            sector=args.sector,
            contact=args.contact,
            phone=args.phone,
            email=args.email,
            package=args.package,
            weekly_leads=args.weekly_leads,
            notes=args.notes,
        )
        print(f"CLIENT_INTAKE_OK | slug={intake['client_slug']} | package={intake['package']}")
        print(f"Files written to: company/runtime/clients/{intake['client_slug']}/")
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
