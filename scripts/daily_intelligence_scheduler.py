"""
Daily Intelligence Scheduler

Runs every morning and generates:
- Saudi prospect batch scoring
- Revenue pipeline analysis
- CEO daily brief markdown

Can be invoked as a standalone script or via APScheduler.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Ensure repo root is on path when running script directly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from intelligence import RevenueIntelligenceEngine, SaudiMarketIntelligence
from intelligence.saudi_market_intelligence import SaudiCompanyProfile


PROSPECTS_PATH = Path("data/commercial/saudi_prospects_sample.json")
PIPELINE_PATH = Path("data/commercial/pipeline_sample.json")
OUTPUT_DIR = Path("reports/daily_intelligence")


def load_prospects(path: Path = PROSPECTS_PATH) -> list[SaudiCompanyProfile]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return [
        SaudiCompanyProfile(
            company_name=item["company_name"],
            sector=item["sector"],
            city=item["city"],
            employees_estimate=item.get("employees_estimate"),
            website=item.get("website"),
        )
        for item in raw
    ]


def load_pipeline(path: Path = PIPELINE_PATH) -> list:
    if not path.exists():
        return []
    raw = json.loads(path.read_text(encoding="utf-8"))
    from intelligence import Deal
    now = datetime.utcnow()
    return [
        Deal(
            deal_id=d["deal_id"],
            company_name=d["company_name"],
            stage=d["stage"],
            value_sar=d["value_sar"],
            created_at=datetime.fromisoformat(d.get("created_at", now.isoformat())),
            last_activity_at=datetime.fromisoformat(d.get("last_activity_at", now.isoformat())),
            activities_count=d.get("activities_count", 0),
            days_in_stage=d.get("days_in_stage", 0),
        )
        for d in raw
    ]


def run_daily_intelligence(prospects_path: Path = PROSPECTS_PATH, pipeline_path: Path = PIPELINE_PATH, output_dir: Path = OUTPUT_DIR) -> dict[str, Any]:
    """Run the full daily intelligence batch."""
    output_dir.mkdir(parents=True, exist_ok=True)
    date_slug = datetime.utcnow().strftime("%Y-%m-%d")

    # Score prospects
    intel = SaudiMarketIntelligence()
    prospects = load_prospects(prospects_path)
    scored = [intel.score_icp(p) for p in prospects]
    top_prospects = sorted(scored, key=lambda s: s.score, reverse=True)[:10]

    # Analyze pipeline
    engine = RevenueIntelligenceEngine()
    engine.load_deals(load_pipeline(pipeline_path))
    revenue_intel = engine.analyze()

    # Build brief
    brief = {
        "generated_at": datetime.utcnow().isoformat(),
        "top_prospects": [
            {
                "company": s.company_name,
                "score": s.score,
                "recommended_package": intel.recommend_entry(prospects[i].sector, prospects[i].city)["recommended_package"],
            }
            for i, s in enumerate(top_prospects)
        ],
        "pipeline": {
            "health": revenue_intel.pipeline_health,
            "total_pipeline_sar": revenue_intel.total_pipeline_sar,
            "weighted_pipeline_sar": revenue_intel.weighted_pipeline_sar,
            "revenue_at_risk_sar": revenue_intel.revenue_at_risk_sar,
            "recommended_actions": revenue_intel.recommended_actions,
        },
    }

    output_path = output_dir / f"daily_brief_{date_slug}.json"
    output_path.write_text(json.dumps(brief, indent=2, ensure_ascii=False), encoding="utf-8")

    md_path = output_dir / f"daily_brief_{date_slug}.md"
    md_path.write_text(render_brief_markdown(brief), encoding="utf-8")

    return brief


def render_brief_markdown(brief: dict[str, Any]) -> str:
    lines = [
        "# Dealix CEO Daily Brief",
        "",
        f"Generated: {brief['generated_at']}",
        "",
        "## Pipeline Intelligence",
        "",
        f"- **Health:** {brief['pipeline']['health']:.1f}/100",
        f"- **Total Pipeline:** SAR {brief['pipeline']['total_pipeline_sar']:,.2f}",
        f"- **Weighted Pipeline:** SAR {brief['pipeline']['weighted_pipeline_sar']:,.2f}",
        f"- **Revenue at Risk:** SAR {brief['pipeline']['revenue_at_risk_sar']:,.2f}",
        "",
        "### Recommended Actions",
        "",
    ]
    for action in brief["pipeline"]["recommended_actions"]:
        lines.append(f"- {action}")
    lines.extend(["", "## Top Saudi Prospects", ""])
    for p in brief["top_prospects"]:
        lines.append(f"- **{p['company']}** — Score {p['score']:.1f} → {p['recommended_package']}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Dealix Daily Intelligence Scheduler")
    parser.add_argument("--prospects", type=Path, default=PROSPECTS_PATH)
    parser.add_argument("--pipeline", type=Path, default=PIPELINE_PATH)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT_DIR)
    args = parser.parse_args()

    brief = run_daily_intelligence(args.prospects, args.pipeline, args.output_dir)
    print(json.dumps(brief, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
