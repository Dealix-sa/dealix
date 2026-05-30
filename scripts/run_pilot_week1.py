#!/usr/bin/env python3
"""
CLI: Start and manage a 499 SAR 7-day pilot.
استخدام: python scripts/run_pilot_week1.py --start --company "اسم الشركة" --payment-ref MOYASAR-XXX

Commands:
  --start       Start a new pilot (requires payment confirmation)
  --brief       Show today's tasks for an active pilot
  --build-proof Build proof pack at end of pilot
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Dealix 7-day Pilot Delivery Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start a new pilot (after payment confirmed)
  python scripts/run_pilot_week1.py --start \\
    --company "وكالة الإبداع" --contact "أحمد" \\
    --payment-ref "MOYASAR-INV-001" \\
    --sector marketing_agency \\
    --pain "تأخر الرد على العملاء"

  # Get today's brief for active pilot
  python scripts/run_pilot_week1.py --brief --pilot-id PILOT-UUID --day 3

  # Build proof pack at end of pilot
  python scripts/run_pilot_week1.py --build-proof \\
    --pilot-id PILOT-UUID \\
    --messages-drafted 6 --messages-sent 6 --replies 2 --meetings 1
        """,
    )

    # Mode
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument("--start", action="store_true", help="Start a new pilot")
    mode_group.add_argument("--brief", action="store_true", help="Get today's task brief")
    mode_group.add_argument("--build-proof", action="store_true", help="Build proof pack")
    mode_group.add_argument("--list", action="store_true", help="List active pilots")

    # Start options
    parser.add_argument("--company", help="Company name")
    parser.add_argument("--contact", default="", help="Contact person name")
    parser.add_argument("--sector", default="other", help="Company sector")
    parser.add_argument("--pain", default="", help="Pain points")
    parser.add_argument("--payment-ref", help="Moyasar invoice ID or bank transfer ref")
    parser.add_argument("--amount", type=float, default=499.0, help="Amount in SAR (default: 499)")

    # Brief options
    parser.add_argument("--pilot-id", help="Pilot ID")
    parser.add_argument("--day", type=int, default=1, help="Current day (1-7)")

    # Proof build options
    parser.add_argument("--messages-drafted", type=int, default=0)
    parser.add_argument("--messages-sent", type=int, default=0)
    parser.add_argument("--replies", type=int, default=0)
    parser.add_argument("--meetings", type=int, default=0)
    parser.add_argument("--rt-before", type=float, default=0.0, help="Response time before (hours)")
    parser.add_argument("--rt-after", type=float, default=0.0, help="Response time after (hours)")
    parser.add_argument("--deals", type=int, default=0)

    return parser.parse_args()


def cmd_start(args: argparse.Namespace) -> None:
    if not args.company:
        print("❌ --company required for --start")
        sys.exit(1)
    if not args.payment_ref:
        print("❌ --payment-ref required (NO_LIVE_CHARGE gate: payment must be confirmed)")
        sys.exit(1)

    import uuid
    from dealix.commercial.pilot_delivery import PilotContext, build_pilot_plan, save_pilot

    pilot_id = str(uuid.uuid4())
    ctx = PilotContext(
        pilot_id=pilot_id,
        account_id=str(uuid.uuid4()),
        company_name=args.company,
        contact_name=args.contact,
        sector=args.sector,
        pain_points=args.pain,
        amount_sar=args.amount,
        payment_ref=args.payment_ref,
        payment_confirmed=True,
    )

    plan = build_pilot_plan(ctx)
    save_pilot(plan)

    print(f"\n✅ تم بدء البرنامج التجريبي / Pilot started!")
    print(f"   🆔 Pilot ID: {plan.pilot_id}")
    print(f"   🏢 Company:  {plan.company_name}")
    print(f"   💰 Amount:   {args.amount} SAR")
    print(f"   📋 Payment:  {args.payment_ref}")
    print()
    print("📅 اليوم الأول / Day 1 Tasks:")
    day1 = plan.days[0]
    for task in day1.tasks_ar:
        print(f"   • {task}")
    print(f"\n✔️  المُخرج / Deliverable: {day1.deliverable_ar}")
    print()
    print(f"احفظ معرف البرنامج: python scripts/run_pilot_week1.py --brief --pilot-id {pilot_id} --day 1")
    print()
    # Also save markdown
    md_path = f"data/pilots/{pilot_id}_plan.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(plan.to_markdown_ar())
    print(f"📄 Full plan saved: {md_path}")


def cmd_brief(args: argparse.Namespace) -> None:
    if not args.pilot_id:
        print("❌ --pilot-id required for --brief")
        sys.exit(1)

    plan_path = f"data/pilots/{args.pilot_id}.json"
    if not os.path.exists(plan_path):
        print(f"❌ Pilot {args.pilot_id} not found in data/pilots/")
        sys.exit(1)

    from dealix.commercial.pilot_delivery import PilotPlan, get_day_brief

    with open(plan_path, encoding="utf-8") as f:
        plan_data = json.load(f)

    # Rebuild plan from data
    from dealix.commercial.pilot_delivery import DayTask
    days = []
    for d in plan_data["days"]:
        days.append(DayTask(
            day=d["day"],
            title_ar=d["title_ar"],
            title_en=d["title_en"],
            tasks_ar=d["tasks_ar"],
            tasks_en=d["tasks_en"],
            deliverable_ar=d["deliverable_ar"],
            deliverable_en=d["deliverable_en"],
            requires_approval=d.get("requires_approval", False),
        ))

    from datetime import UTC, datetime
    plan = PilotPlan(
        pilot_id=plan_data["pilot_id"],
        account_id=plan_data["account_id"],
        company_name=plan_data["company_name"],
        days=days,
        payment_confirmed=plan_data.get("payment_confirmed", True),
        created_at=datetime.fromisoformat(plan_data["created_at"]),
    )

    brief = get_day_brief(plan, args.day)

    print(f"\n{'='*60}")
    print(f"اليوم {brief['day']} — {brief['title_ar']}")
    print(f"الشركة: {brief['company']}")
    print(f"{'='*60}\n")
    print("المهام / Tasks:")
    for task in brief["tasks_ar"]:
        print(f"  • {task}")
    print(f"\n✔️  المُخرج / Deliverable: {brief['deliverable_ar']}")
    if brief.get("requires_approval"):
        print("\n⚠️  يتطلب موافقة الفاوندر قبل أي إرسال")
    print()


def cmd_build_proof(args: argparse.Namespace) -> None:
    if not args.pilot_id:
        print("❌ --pilot-id required for --build-proof")
        sys.exit(1)

    plan_path = f"data/pilots/{args.pilot_id}.json"
    if not os.path.exists(plan_path):
        print(f"❌ Pilot {args.pilot_id} not found")
        sys.exit(1)

    with open(plan_path, encoding="utf-8") as f:
        plan_data = json.load(f)

    from dealix.commercial.proof_builder import ProofEvidence, build_proof_pack

    evidence = ProofEvidence(
        messages_drafted=args.messages_drafted,
        messages_sent=args.messages_sent,
        replies_received=args.replies,
        meetings_booked=args.meetings,
        deals_created=args.deals,
        response_time_before_hours=args.rt_before,
        response_time_after_hours=args.rt_after,
    )

    pack = build_proof_pack(
        pilot_id=args.pilot_id,
        account_id=plan_data.get("account_id", ""),
        company_name=plan_data["company_name"],
        contact_name="",
        sector="other",
        pain_point="",
        evidence=evidence,
    )

    print(f"\n✅ تم بناء طقم الإثبات / Proof pack built!")
    print(f"   🆔 Pack ID: {pack.pack_id}")
    print(f"   📊 Evidence Level: L{pack.evidence_level} ({pack.evidence_level_name})")
    print(f"   ✔️  Complete: {pack.is_complete}")
    print(f"   📸 Case Study Eligible: {pack.can_use_as_case_study}")
    print()
    print("النتائج / Results:")
    print(f"  رسائل مُرسلة: {pack.messages_sent}")
    print(f"  ردود واردة: {pack.replies_received}")
    print(f"  اجتماعات: {pack.meetings_booked}")
    print(f"  تحسّن وقت الاستجابة: {pack.response_time_improvement}")
    print()
    print(f"📄 Markdown: data/proof-packs/{pack.pack_id}_ar.md")
    print(f"📊 JSON: data/proof-packs/{pack.pack_id}.json")


def cmd_list() -> None:
    pilots_dir = "data/pilots"
    if not os.path.exists(pilots_dir):
        print("No pilots found (data/pilots/ doesn't exist)")
        return

    pilots = [f for f in os.listdir(pilots_dir) if f.endswith(".json")]
    if not pilots:
        print("No active pilots")
        return

    print(f"\n{'='*60}")
    print(f"Active Pilots ({len(pilots)})")
    print(f"{'='*60}")
    for pilot_file in pilots:
        try:
            with open(os.path.join(pilots_dir, pilot_file), encoding="utf-8") as f:
                data = json.load(f)
            print(f"  🆔 {data['pilot_id'][:8]}... | 🏢 {data['company_name']} | 💰 {data.get('amount_sar', 499)} SAR")
        except Exception:
            print(f"  ❌ Could not read {pilot_file}")
    print()


def main() -> None:
    args = parse_args()

    if args.start:
        cmd_start(args)
    elif args.brief:
        cmd_brief(args)
    elif args.build_proof:
        cmd_build_proof(args)
    elif args.list:
        cmd_list()


if __name__ == "__main__":
    main()
