"""CLI for Dealix Commercial Intelligence.

Usage:
    python -m cli.sales_strategist --company "Najm Tech" --sector software --city Riyadh --employees 45 --website https://najmtech.sa
    python -m cli.sales_strategist --batch data/saudi_prospects.json
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

from intelligence import SaudiCompanyProfile, SaudiMarketIntelligence


def score_one(company_name: str, sector: str, city: str, employees: int | None, website: str | None) -> dict:
    profile = SaudiCompanyProfile(
        company_name=company_name,
        sector=sector,
        city=city,
        employees_estimate=employees,
        website=website,
    )
    intel = SaudiMarketIntelligence()
    score = intel.score_icp(profile)
    entry = intel.recommend_entry(sector, city)
    return {
        "company_name": score.company_name,
        "icp_score": score.score,
        "reasons": score.reasons,
        "risk_flags": score.risk_flags,
        "momentum": entry["momentum"],
        "recommended_package": entry["recommended_package"],
        "next_action": entry["next_action"],
    }


def run_batch(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    results = []
    for item in data:
        results.append(score_one(
            company_name=item["company_name"],
            sector=item["sector"],
            city=item["city"],
            employees=item.get("employees_estimate"),
            website=item.get("website"),
        ))
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Dealix Sales Strategist CLI")
    parser.add_argument("--company", type=str, help="Company name")
    parser.add_argument("--sector", type=str, help="Sector (e.g., software, fintech)")
    parser.add_argument("--city", type=str, help="City (e.g., Riyadh, Jeddah)")
    parser.add_argument("--employees", type=int, default=None, help="Employee count estimate")
    parser.add_argument("--website", type=str, default=None, help="Company website")
    parser.add_argument("--batch", type=Path, default=None, help="Path to JSON batch file")
    parser.add_argument("--output", type=Path, default=None, help="Output JSON file")
    args = parser.parse_args()

    if args.batch:
        results = run_batch(args.batch)
    elif args.company and args.sector and args.city:
        results = [score_one(args.company, args.sector, args.city, args.employees, args.website)]
    else:
        parser.print_help()
        return 1

    output = json.dumps(results, indent=2, ensure_ascii=False)
    if args.output:
        args.output.write_text(output, encoding="utf-8")
        print(f"Wrote {len(results)} results to {args.output}")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
