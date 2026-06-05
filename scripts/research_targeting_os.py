#!/usr/bin/env python3
"""
research_targeting_os.py — Dealix Market Intelligence & Targeting OS orchestrator.

Runs the daily pipeline end-to-end and writes founder-review artifacts. It is
deliberately *read-only and offline by default*: it never sends a message, never
charges anyone, and discovery is disabled unless explicitly enabled with network
credentials. The big rule:

    Search broadly, filter strictly, send rarely, evidence everything.

Pipeline:
    seed/discover -> normalize+dedupe -> compliance gate -> score -> route
    -> founder shortlist -> drafts (needs_approval) -> daily brief

Outputs (under --out):
    company_master.jsonl · ranked_targets.csv · daily_targeting_brief.md
    founder_shortlist.md · drafts_for_review.md · tomorrow_targeting_plan.md

Usage:
    python scripts/research_targeting_os.py --seed data/targeting/company_seed_template.csv \
        --out data/targeting/out --top 80
    python scripts/research_targeting_os.py --discover --queries-file data/targeting/queries.txt \
        --out data/targeting/out --top 80   # discovery is a no-op without a provider
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from scripts.targeting_compliance_gate import gate_company, load_blocked  # noqa: E402
from scripts.targeting_daily_brief import render_brief  # noqa: E402
from scripts.targeting_draft_lab import (  # noqa: E402
    _signal_angles,
    build_draft,
    eligible_for_draft,
)
from scripts.targeting_enrichment import load_seed_csv, normalize_and_dedupe  # noqa: E402
from scripts.targeting_scorecard import (  # noqa: E402
    _load_signal_weights,
    load_weights,
    score_and_merge,
)


def discover_candidates(queries: list[str], *, allow_network: bool) -> list[dict[str, Any]]:
    """Discovery stub.

    By design this returns nothing unless a compliant provider is wired in AND
    network is explicitly allowed. Discovery providers (e.g. Google Programmable
    Search JSON API) must: respect robots.txt and site terms, use only public
    pages, require an API key + CX from env, and be replaceable. We keep the
    daily loop fully functional on the founder seed file alone.
    """
    if not allow_network:
        print(
            "[discover] network disabled — running on seed file only. "
            "Wire a compliant provider + --allow-network to enable discovery.",
            file=sys.stderr,
        )
        return []
    # Intentionally not implemented here: enabling discovery requires a vetted,
    # robots-respecting provider behind an explicit founder decision.
    print(
        f"[discover] {len(queries)} queries queued but no compliant provider configured.",
        file=sys.stderr,
    )
    return []


def run_pipeline(
    *,
    seed: Path | None,
    queries: list[str] | None,
    phase: int,
    allow_network: bool,
    top: int,
) -> dict[str, Any]:
    """Execute the pipeline and return all artifacts as in-memory objects."""
    weights = load_weights()
    sig_w = _load_signal_weights()
    policy = load_blocked()
    angles = _signal_angles()

    # 1) Gather raw candidates
    raw: list[dict[str, Any]] = []
    if seed and seed.exists():
        raw.extend(load_seed_csv(seed))
    raw_from_discovery = discover_candidates(queries or [], allow_network=allow_network)
    raw.extend(raw_from_discovery)
    raw_count = len(raw)

    # 2) Normalize + dedupe
    companies = normalize_and_dedupe(raw, phase=phase)

    # 3) Compliance gate (drop rejects, flag review)
    gated: list[dict[str, Any]] = []
    for c in companies:
        result = gate_company(c, policy)
        c["risk_flags"] = sorted(set((c.get("risk_flags") or []) + result["risk_flags"]))
        c["compliance_status"] = result["status"]
        if result["status"] == "reject":
            c["draft_status"] = "rejected"
            continue
        # keep only compliant evidence
        if result["allowed_sources"]:
            c["source_urls"] = result["allowed_sources"]
            c["evidence_count"] = len(result["allowed_sources"])
        gated.append(c)

    # 4) Score + route
    scored = [score_and_merge(c, weights=weights, signal_weights=sig_w) for c in gated]
    scored.sort(key=lambda r: r["targeting_score"], reverse=True)
    scored = scored[:top] if top else scored

    # 5) Founder shortlist
    shortlist = [
        c
        for c in scored
        if str(c.get("grade")) in {"A+", "A"} and c.get("compliance_status") == "approved"
    ]

    # 6) Drafts (needs_approval only; clean only)
    drafts: list[dict[str, Any]] = []
    for c in shortlist:
        ok, _ = eligible_for_draft(c)
        if not ok:
            continue
        d = build_draft(c, angles)
        if not d["violations"]:
            drafts.append(d)

    return {
        "raw_count": raw_count,
        "companies": scored,
        "shortlist": shortlist,
        "drafts": drafts,
    }


# --------------------------------------------------------------------------- #
# Artifact writers
# --------------------------------------------------------------------------- #
def write_company_master(companies: list[dict[str, Any]], path: Path) -> None:
    lines = [
        json.dumps({k: v for k, v in c.items() if not k.startswith("_")}, ensure_ascii=False)
        for c in companies
    ]
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def write_ranked_csv(companies: list[dict[str, Any]], path: Path) -> None:
    cols = [
        "company_name",
        "website",
        "city",
        "sector",
        "targeting_score",
        "grade",
        "recommended_offer",
        "evidence_count",
        "compliance_status",
        "next_action",
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for c in companies:
            w.writerow({k: c.get(k, "") for k in cols})


def write_shortlist_md(shortlist: list[dict[str, Any]], path: Path) -> None:
    lines = [
        "# Dealix Founder Shortlist",
        "",
        "> راجع هذه الشركات يدويًا. لا إرسال بدون موافقة.",
        "",
    ]
    for i, c in enumerate(shortlist, 1):
        lines.append(
            f"{i}. **{c.get('company_name')}** — {c.get('sector')} — "
            f"score {c.get('targeting_score')} ({c.get('grade')}) — "
            f"offer: {c.get('recommended_offer','—')} — "
            f"evidence: {c.get('evidence_count',0)}"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_drafts_md(drafts: list[dict[str, Any]], path: Path) -> None:
    from scripts.targeting_draft_lab import render_drafts_markdown

    path.write_text(render_drafts_markdown(drafts) + "\n", encoding="utf-8")


def write_tomorrow_plan(result: dict[str, Any], path: Path) -> None:
    companies = result["companies"]
    top_sector = companies[0].get("sector") if companies else "b2b_consulting"
    lines = [
        "# Tomorrow's Targeting Plan",
        "",
        f"- Lead with **{top_sector}** in Riyadh (highest avg score today).",
        "- Require >=2 independent evidence sources before any draft.",
        "- Prefer Proof-gap and Revenue-leakage angles over generic AI automation.",
        "- Manual sends only, founder-approved, opt-out respected.",
        "",
        "## Stop Doing",
        "- No single-source targets. No auto-sends. No scraping behind login.",
        "",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_artifacts(result: dict[str, Any], out_dir: Path) -> dict[str, str]:
    out_dir.mkdir(parents=True, exist_ok=True)
    companies = result["companies"]
    paths = {
        "company_master": out_dir / "company_master.jsonl",
        "ranked": out_dir / "ranked_targets.csv",
        "brief": out_dir / "daily_targeting_brief.md",
        "shortlist": out_dir / "founder_shortlist.md",
        "drafts": out_dir / "drafts_for_review.md",
        "tomorrow": out_dir / "tomorrow_targeting_plan.md",
    }
    write_company_master(companies, paths["company_master"])
    write_ranked_csv(companies, paths["ranked"])
    paths["brief"].write_text(
        render_brief(
            companies,
            raw_candidates=result["raw_count"],
            drafts=len(result["drafts"]),
            manual_sends=min(5, len(result["drafts"])),
        )
        + "\n",
        encoding="utf-8",
    )
    write_shortlist_md(result["shortlist"], paths["shortlist"])
    write_drafts_md(result["drafts"], paths["drafts"])
    write_tomorrow_plan(result, paths["tomorrow"])
    return {k: str(v) for k, v in paths.items()}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Dealix Market Intelligence & Targeting OS")
    ap.add_argument(
        "--seed", default=str(_ROOT / "data" / "targeting" / "company_seed_template.csv")
    )
    ap.add_argument(
        "--discover", action="store_true", help="enable discovery (needs provider+network)"
    )
    ap.add_argument("--queries-file", default=None)
    ap.add_argument("--allow-network", action="store_true", help="permit discovery network calls")
    ap.add_argument("--phase", type=int, default=1)
    ap.add_argument("--top", type=int, default=80)
    ap.add_argument("--out", default=str(_ROOT / "data" / "targeting" / "out"))
    args = ap.parse_args(argv)

    queries: list[str] = []
    if args.discover and args.queries_file and Path(args.queries_file).exists():
        queries = [
            ln.strip()
            for ln in Path(args.queries_file).read_text(encoding="utf-8").splitlines()
            if ln.strip() and not ln.strip().startswith("#")
        ]

    result = run_pipeline(
        seed=Path(args.seed) if args.seed else None,
        queries=queries,
        phase=args.phase,
        allow_network=args.allow_network,
        top=args.top,
    )
    paths = write_artifacts(result, Path(args.out))

    print(
        json.dumps(
            {
                "raw_candidates": result["raw_count"],
                "clean_companies": len(result["companies"]),
                "shortlist": len(result["shortlist"]),
                "drafts": len(result["drafts"]),
                "outputs": paths,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
