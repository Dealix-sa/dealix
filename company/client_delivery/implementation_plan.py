#!/usr/bin/env python3
"""
Client Delivery — Implementation Plan Generator

Generates a 14-day implementation plan for a client Pilot.
Output: company/runtime/clients/{slug}/implementation/

Usage:
    python company/client_delivery/implementation_plan.py \
        --client <slug> \
        --system "WhatsApp Revenue OS" \
        --start-date 2026-06-28 \
        --team-size 5
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLIENTS_DIR = ROOT / "company" / "runtime" / "clients"

SYSTEM_PLANS: dict[str, dict] = {
    "whatsapp_revenue_os": {
        "label": "WhatsApp Revenue OS",
        "week1": [
            "ربط WhatsApp Business API أو استيراد الرسائل",
            "تصنيف العملاء المحتملين حسب الأولوية",
            "بناء قوالب الرسائل المخصصة للقطاع",
            "إعداد لوحة المتابعة اليومية",
            "اختبار أولي مع 20 عميل",
        ],
        "week2": [
            "توسيع التشغيل لكل قاعدة العملاء",
            "تدريب الفريق على اللوحة اليومية",
            "مراجعة معدلات الاستجابة والتحويل",
            "تعديل القوالب بناءً على النتائج",
            "تقرير نتائج Pilot + توصية الاستمرار",
        ],
        "success_metrics": [
            "معدل الاستجابة للاستفسارات < 4 ساعات",
            "0 استفسار يضيع دون متابعة",
            "تقرير يومي يعمل كل صباح",
        ],
    },
    "crm_followup_os": {
        "label": "CRM Follow-Up OS",
        "week1": [
            "استيراد بيانات العملاء المحتملين وتنظيفها",
            "بناء pipeline المبيعات (5 مراحل)",
            "ضبط تذكيرات المتابعة التلقائية",
            "تصنيف الفرص حسب الأولوية",
            "اختبار مع الفريق",
        ],
        "week2": [
            "تشغيل كامل مع كل الفريق",
            "بناء تقرير أسبوعي للمدير",
            "مراجعة معدلات تحويل المراحل",
            "تعديل معايير التصنيف",
            "تقرير نتائج Pilot + توصية",
        ],
        "success_metrics": [
            "100% من الفرص موثقة في النظام",
            "لا فرصة بدون تاريخ متابعة",
            "تقرير أسبوعي يُرسَل تلقائيًا (كمسودة)",
        ],
    },
    "revenue_command_center": {
        "label": "Revenue Command Center",
        "week1": [
            "بناء لوحة اليومية للمؤسس",
            "ربط مصادر البيانات (استفسارات، عروض، إغلاق)",
            "إعداد تنبيهات الفرص المعلقة",
            "تقرير صباحي يومي",
            "اختبار مع المؤسس",
        ],
        "week2": [
            "توسيع اللوحة لتشمل الفريق",
            "بناء تقرير أسبوعي للأداء",
            "ضبط مقاييس الأداء الرئيسية (KPIs)",
            "تدريب الفريق",
            "تقرير نتائج Pilot",
        ],
        "success_metrics": [
            "المؤسس يرى الأولويات كل صباح خلال 5 دقائق",
            "0 فرصة تمر دون تنبيه",
            "تقرير أسبوعي يعمل تلقائيًا",
        ],
    },
}

DEFAULT_PLAN = {
    "label": "نظام مخصص",
    "week1": [
        "جلسة تحديد النطاق التفصيلي",
        "بناء البنية الأساسية",
        "اختبار وحدات النظام",
        "تكامل مع الأدوات الحالية",
        "مراجعة أولية مع الفريق",
    ],
    "week2": [
        "تشغيل تجريبي كامل",
        "تدريب الفريق",
        "تعديلات بناءً على الملاحظات",
        "توثيق النظام",
        "تقرير النتائج والتوصية",
    ],
    "success_metrics": [
        "النظام يعمل كما هو مخطط",
        "الفريق يستخدم النظام يوميًا",
        "نتائج قابلة للقياس",
    ],
}


def generate_plan(
    slug: str,
    system: str,
    start_date: date,
    team_size: int = 5,
) -> dict:
    intake_path = CLIENTS_DIR / slug / "intake.json"
    if not intake_path.exists():
        raise FileNotFoundError(f"Client not found: {slug}")
    intake = json.loads(intake_path.read_text())

    system_key = system.lower().replace(" ", "_").replace("-", "_")
    plan_template = SYSTEM_PLANS.get(system_key, DEFAULT_PLAN)

    week1_days = []
    for i, task in enumerate(plan_template["week1"]):
        task_date = start_date + timedelta(days=i)
        week1_days.append({"day": i + 1, "date": task_date.isoformat(), "task": task, "done": False})

    week2_start = start_date + timedelta(days=7)
    week2_days = []
    for i, task in enumerate(plan_template["week2"]):
        task_date = week2_start + timedelta(days=i)
        week2_days.append({"day": i + 8, "date": task_date.isoformat(), "task": task, "done": False})

    end_date = start_date + timedelta(days=13)

    plan = {
        "client_slug": slug,
        "company_name": intake["company_name"],
        "system": system,
        "system_label": plan_template["label"],
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "team_size": team_size,
        "week1_tasks": week1_days,
        "week2_tasks": week2_days,
        "success_metrics": plan_template["success_metrics"],
        "created_date": date.today().isoformat(),
    }

    out_dir = CLIENTS_DIR / slug / "implementation"
    out_dir.mkdir(parents=True, exist_ok=True)

    (out_dir / "plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2))
    (out_dir / "IMPLEMENTATION_PLAN.md").write_text(_render_plan(plan))
    (out_dir / "DELIVERY_CHECKLIST.md").write_text(_render_checklist(plan))

    intake["pilot_start"] = start_date.isoformat()
    intake["pilot_end"] = end_date.isoformat()
    (CLIENTS_DIR / slug / "intake.json").write_text(
        json.dumps(intake, ensure_ascii=False, indent=2)
    )

    return plan


def _render_plan(p: dict) -> str:
    w1 = "\n".join(
        f"| اليوم {t['day']} | {t['date']} | {t['task']} |"
        for t in p["week1_tasks"]
    )
    w2 = "\n".join(
        f"| اليوم {t['day']} | {t['date']} | {t['task']} |"
        for t in p["week2_tasks"]
    )
    metrics = "\n".join(f"- ✅ {m}" for m in p["success_metrics"])

    return f"""# خطة التنفيذ — {p['company_name']}

**النظام**: {p['system_label']}
**البداية**: {p['start_date']}
**النهاية**: {p['end_date']}
**حجم الفريق**: {p['team_size']} أشخاص

---

## الأسبوع الأول: البناء والإعداد

| اليوم | التاريخ | المهمة |
|------|---------|-------|
{w1}

---

## الأسبوع الثاني: التشغيل والمراجعة

| اليوم | التاريخ | المهمة |
|------|---------|-------|
{w2}

---

## معايير النجاح

{metrics}

---

## التزامات الطرفين

### Dealix تلتزم بـ:
- تسليم كل مهام الأسبوع الأول في موعدها
- تقديم تقارير يومية عن التقدم
- دعم فوري لأي مشكلة تقنية
- تعديل الخطة إذا تغيرت الأولويات

### {p['company_name']} تلتزم بـ:
- توفير البيانات والوصول المطلوب في اليوم الأول
- وجود شخص مسؤول للتواصل اليومي
- مراجعة المخرجات خلال 24 ساعة من التسليم
- تزويدنا بالملاحظات بشكل فوري

---

*Dealix | {p['created_date']}*
"""


def _render_checklist(p: dict) -> str:
    w1_checks = "\n".join(f"- [ ] يوم {t['day']}: {t['task']}" for t in p["week1_tasks"])
    w2_checks = "\n".join(f"- [ ] يوم {t['day']}: {t['task']}" for t in p["week2_tasks"])
    metrics_checks = "\n".join(f"- [ ] {m}" for m in p["success_metrics"])

    return f"""# قائمة التسليم — {p['company_name']}

**النظام**: {p['system_label']}
**الفترة**: {p['start_date']} → {p['end_date']}

---

## الأسبوع الأول

{w1_checks}

## الأسبوع الثاني

{w2_checks}

---

## معايير قبول Pilot

{metrics_checks}

---

## مخرجات التسليم النهائية

- [ ] تقرير نتائج Pilot (PDF أو Markdown)
- [ ] دليل التشغيل اليومي
- [ ] توصية المرحلة التالية
- [ ] عرض أسعار Retainer (إن كان مناسبًا)

---

*Dealix | {p['created_date']}*
"""


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate implementation plan")
    p.add_argument("--client", required=True)
    p.add_argument("--system", required=True, help="System name (e.g. 'WhatsApp Revenue OS')")
    p.add_argument("--start-date", required=True, help="YYYY-MM-DD")
    p.add_argument("--team-size", type=int, default=5)
    return p.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    try:
        start = date.fromisoformat(args.start_date)
        result = generate_plan(
            slug=args.client,
            system=args.system,
            start_date=start,
            team_size=args.team_size,
        )
        print(f"PLAN_OK | client={result['client_slug']} | {result['start_date']} → {result['end_date']}")
        print(f"Files: company/runtime/clients/{result['client_slug']}/implementation/")
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"ERROR: Invalid date format: {e}", file=sys.stderr)
        sys.exit(1)
