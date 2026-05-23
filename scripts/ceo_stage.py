#!/usr/bin/env python3
"""Determine the current 90-day stage for the Dealix founder.

Stage logic (per docs/founder/CEO_90_DAY_STRATEGIC_PLAN.md):

  0 paid sprints                        -> Stage 1 (Proof of Interest, days 1-7)
  1 paid sprint                         -> Stage 2 (Proof of Conversion, days 8-30)
  2-3 paid + 0 deliveries               -> Stage 2 (still converting)
  2-3 paid + 1+ deliveries              -> Stage 3 (Proof of Delivery, 31-60)
  3+ paid + 1+ retainer attempt         -> Stage 4 (Proof of Retention, 61-90)

Stdlib only. Bilingual output.
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
PRIVATE = REPO_ROOT / "dealix-ops-private"

CASH_CSV = PRIVATE / "revenue" / "cash_collected.csv"
DELIVERY_QA_DIR = PRIVATE / "delivery" / "qa"
MRR_CSV = PRIVATE / "revenue" / "mrr_tracker.csv"


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    try:
        with path.open(encoding="utf-8") as fh:
            return list(csv.DictReader(fh))
    except (OSError, csv.Error):
        return []


def count_paid_sprints() -> int:
    rows = _read_csv(CASH_CSV)
    paid = 0
    for r in rows:
        status = (r.get("status") or "").strip().lower()
        if status in {"paid", "collected", "received"}:
            paid += 1
    return paid


def count_deliveries() -> int:
    if not DELIVERY_QA_DIR.exists() or not DELIVERY_QA_DIR.is_dir():
        return 0
    return sum(
        1
        for p in DELIVERY_QA_DIR.iterdir()
        if p.is_file() and not p.name.startswith(".") and p.name != ".gitkeep"
    )


def count_retainer_attempts() -> int:
    rows = _read_csv(MRR_CSV)
    attempts = 0
    for r in rows:
        status = (r.get("status") or "").strip().lower()
        if status in {"active", "pending", "proposed", "offered"}:
            attempts += 1
    return attempts


def determine_stage(paid: int, deliveries: int, retainers: int) -> dict:
    if paid == 0:
        return {
            "stage_number": 1,
            "name_en": "Proof of Interest",
            "name_ar": "إثبات الاهتمام",
            "window": "Days 1-7 / أيام 1-7",
            "gates_remaining": [
                "Close first paid sprint (SAR 30k) / إغلاق أول سبرنت مدفوع",
                "Collect 5+ qualified pipeline entries / 5+ فرص مؤهلة في الأنبوب",
            ],
            "next_action_en": "Run founder DM pack on 20 qualified targets this week.",
            "next_action_ar": "نفّذ حزمة رسائل المؤسس على 20 هدفًا مؤهلًا هذا الأسبوع.",
        }
    if paid == 1 or (2 <= paid <= 3 and deliveries == 0):
        return {
            "stage_number": 2,
            "name_en": "Proof of Conversion",
            "name_ar": "إثبات التحويل",
            "window": "Days 8-30 / أيام 8-30",
            "gates_remaining": [
                "Close 2 more paid sprints / إغلاق سبرنتين مدفوعين إضافيين",
                "First delivery QA pass / اجتياز فحص الجودة الأول",
            ],
            "next_action_en": "Schedule kickoff + deliver sprint #1 inside SLA.",
            "next_action_ar": "اعقد جلسة الانطلاق وسلّم السبرنت الأول داخل اتفاقية الخدمة.",
        }
    if 2 <= paid <= 3 and deliveries >= 1:
        return {
            "stage_number": 3,
            "name_en": "Proof of Delivery",
            "name_ar": "إثبات التسليم",
            "window": "Days 31-60 / أيام 31-60",
            "gates_remaining": [
                "Deliver 2 more sprints to QA spec / تسليم سبرنتين إضافيين بمواصفات الجودة",
                "Trigger first retainer ask / إطلاق أول طلب احتفاظ",
            ],
            "next_action_en": "Send retainer ask to the most engaged sprint client.",
            "next_action_ar": "أرسل طلب الاحتفاظ لأكثر عميل تفاعلًا في السبرنت.",
        }
    if paid >= 3 and retainers >= 1:
        return {
            "stage_number": 4,
            "name_en": "Proof of Retention",
            "name_ar": "إثبات الاحتفاظ",
            "window": "Days 61-90 / أيام 61-90",
            "gates_remaining": [
                "Convert 1 retainer to active MRR / تحويل احتفاظ واحد إلى إيراد متكرر فعلي",
                "Productize the highest-leverage sprint / تحويل أفضل سبرنت إلى منتج",
            ],
            "next_action_en": "Close retainer #1 contract and start monthly cycle.",
            "next_action_ar": "أغلق عقد الاحتفاظ الأول وابدأ الدورة الشهرية.",
        }
    # Default fallback (e.g. paid >= 3, no retainer attempt yet).
    return {
        "stage_number": 3,
        "name_en": "Proof of Delivery",
        "name_ar": "إثبات التسليم",
        "window": "Days 31-60 / أيام 31-60",
        "gates_remaining": [
            "Trigger first retainer ask / إطلاق أول طلب احتفاظ",
        ],
        "next_action_en": "Send retainer ask to the most engaged sprint client.",
        "next_action_ar": "أرسل طلب الاحتفاظ لأكثر عميل تفاعلًا في السبرنت.",
    }


def compute() -> dict:
    paid = count_paid_sprints()
    deliveries = count_deliveries()
    retainers = count_retainer_attempts()
    stage = determine_stage(paid, deliveries, retainers)
    stage["inputs"] = {
        "paid_sprints": paid,
        "deliveries": deliveries,
        "retainer_attempts": retainers,
    }
    return stage


def print_human(stage: dict) -> None:
    print("Dealix 90-Day Stage / مرحلة الـ 90 يومًا")
    print("=" * 64)
    print(f"Stage {stage['stage_number']}: {stage['name_en']} / {stage['name_ar']}")
    print(f"Window / النافذة: {stage['window']}")
    print("-" * 64)
    inputs = stage["inputs"]
    print(
        f"paid_sprints={inputs['paid_sprints']}  "
        f"deliveries={inputs['deliveries']}  "
        f"retainer_attempts={inputs['retainer_attempts']}"
    )
    print("-" * 64)
    print("Gates remaining / البوابات المتبقية:")
    for g in stage["gates_remaining"]:
        print(f"  - {g}")
    print("-" * 64)
    print(f"Next action (EN): {stage['next_action_en']}")
    print(f"الإجراء التالي (AR): {stage['next_action_ar']}")


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    stage = compute()
    if "--json" in argv:
        print(json.dumps(stage, ensure_ascii=False, indent=2))
    else:
        print_human(stage)
    return 0


if __name__ == "__main__":
    sys.exit(main())
