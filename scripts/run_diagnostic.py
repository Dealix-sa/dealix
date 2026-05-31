#!/usr/bin/env python3
"""
CLI: Generate a diagnostic report for a Saudi B2B company.
استخدام: python scripts/run_diagnostic.py --company "اسم الشركة" --sector marketing_agency

Generates a bilingual diagnostic report and saves it locally.
Output: Markdown file + JSON ledger entry.

Constitutional: NO_FAKE_PROOF — all content is AI-generated draft,
requires founder review before delivery.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


VALID_SECTORS = [
    "marketing_agency",
    "consulting",
    "real_estate",
    "logistics",
    "events",
    "training",
    "other",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a Dealix diagnostic report for a Saudi B2B company",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/run_diagnostic.py --company "وكالة الإبداع" --sector marketing_agency
  python scripts/run_diagnostic.py --company "مكتب الاستشارات" --sector consulting --pain "فقدان صفقات بسبب تأخر الرد"
  python scripts/run_diagnostic.py --company "Acme Co" --sector other --locale en --output-dir /tmp/diagnostics
        """,
    )
    parser.add_argument("--company", required=True, help="Company name (Arabic or English)")
    parser.add_argument(
        "--sector",
        default="other",
        choices=VALID_SECTORS,
        help=f"Company sector. Options: {', '.join(VALID_SECTORS)}",
    )
    parser.add_argument("--contact", default="", help="Contact person name")
    parser.add_argument("--pain", default="", help="Specific pain points (Arabic or English)")
    parser.add_argument("--website", default="", help="Company website URL")
    parser.add_argument("--employees", type=int, default=0, help="Number of employees")
    parser.add_argument("--leads", type=int, default=0, help="Monthly leads count")
    parser.add_argument("--tools", default="", help="Current tools (CRM, Excel, WhatsApp, etc.)")
    parser.add_argument("--locale", default="ar", choices=["ar", "en"], help="Output language")
    parser.add_argument("--output-dir", default="data/proofs", help="Output directory for reports")
    parser.add_argument("--dry-run", action="store_true", help="Use fallback template (no LLM call)")
    return parser.parse_args()


async def main() -> None:
    args = parse_args()

    print(f"\n{'='*60}")
    print("DEALIX DIAGNOSTIC ENGINE")
    print(f"{'='*60}")
    print(f"الشركة / Company: {args.company}")
    print(f"القطاع / Sector:  {args.sector}")
    print(f"اللغة / Locale:   {args.locale}")
    if args.pain:
        print(f"نقاط الألم / Pain: {args.pain[:60]}...")
    print(f"{'='*60}\n")

    if args.dry_run:
        print("⚠️  Dry-run mode: using fallback template (no LLM call)")
        os.environ.setdefault("ANTHROPIC_API_KEY", "dry_run_placeholder")

    try:
        from dealix.commercial.diagnostic_engine import DiagnosticRequest, generate_diagnostic

        req = DiagnosticRequest(
            company_name=args.company,
            sector=args.sector,
            pain_points=args.pain,
            website_url=args.website,
            employee_count=args.employees,
            monthly_leads=args.leads,
            current_tools=args.tools,
            contact_name=args.contact,
            locale=args.locale,
        )

        print("🔄 جاري توليد التشخيص... / Generating diagnostic...")
        report = await generate_diagnostic(req)

        # Save markdown output
        os.makedirs(args.output_dir, exist_ok=True)
        safe_name = args.company.replace(" ", "_").replace("/", "-")[:30]
        md_path = os.path.join(args.output_dir, f"diagnostic_{safe_name}_{report.report_id[:8]}.md")
        json_path = os.path.join(args.output_dir, f"diagnostic_{safe_name}_{report.report_id[:8]}.json")

        with open(md_path, "w", encoding="utf-8") as f:
            f.write(report.to_markdown_ar())

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(report.to_dict(), f, ensure_ascii=False, indent=2)

        print(f"\n✅ تم توليد التشخيص / Diagnostic generated:")
        print(f"   📄 Markdown: {md_path}")
        print(f"   📊 JSON:     {json_path}")
        print(f"   🆔 Report ID: {report.report_id}")
        print(f"\n{'='*60}")
        print("الملخص التنفيذي / Executive Summary:")
        print(f"{'='*60}")
        print(report.executive_summary_ar)
        print(f"\nالخطوة التالية / Next Step:")
        print(report.next_step_ar)
        print(f"{'='*60}\n")
        print("⚠️  DRAFT STATUS: يتطلب مراجعة الفاوندر قبل التسليم / Requires founder review before delivery")
        print()

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure you're running from the project root directory.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
