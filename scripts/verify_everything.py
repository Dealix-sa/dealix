#!/usr/bin/env python3
"""Dealix master verifier.

Run from repo root:
    python scripts/verify_everything.py

Aggregates every layer of the Company OS into one PASS/FAIL verdict.
Writes the human report to docs/ops/DEALIX_FINAL_READINESS_REPORT.md and
a machine-readable artifact to evals/eval_status.csv.
"""
from __future__ import annotations

import csv
import datetime
import json
import os
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))


@dataclass
class LayerCheck:
    name: str
    kind: str  # "files" | "script" | "build"
    targets: list[str] = field(default_factory=list)
    command: list[str] | None = None
    optional: bool = False

    def run(self) -> tuple[bool, list[str], list[str]]:
        if self.kind == "files":
            missing = [p for p in self.targets if not (REPO_ROOT / p).exists()]
            return (not missing), [], missing
        if self.kind == "script":
            cmd = self.command or [sys.executable, str(REPO_ROOT / self.targets[0])]
            try:
                proc = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True, timeout=120)
            except Exception as exc:
                return (False, [f"command failed: {exc}"], [])
            notes = [(proc.stdout or "").strip(), (proc.stderr or "").strip()]
            notes = [n for n in notes if n]
            return proc.returncode == 0, notes, []
        if self.kind == "build":
            cmd = self.command or []
            try:
                proc = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True, timeout=300)
            except FileNotFoundError:
                return (True if self.optional else False, ["binary not available"], [])
            except Exception as exc:
                return (False, [f"build failed: {exc}"], [])
            notes = [(proc.stdout or "").strip()[-400:], (proc.stderr or "").strip()[-400:]]
            notes = [n for n in notes if n]
            combined = " ".join(notes).lower()
            if proc.returncode != 0 and ("not found" in combined or "command not found" in combined or "next: not found" in combined):
                return (True if self.optional else False, notes + ["binary not available"], [])
            return proc.returncode == 0, notes, []
        return False, [f"unknown kind: {self.kind}"], []


def all_pages() -> list[str]:
    return [
        "apps/web/app/page.tsx",
        "apps/web/app/ceo/page.tsx",
        "apps/web/app/ceo-os/page.tsx",
        "apps/web/app/founder-leverage/page.tsx",
        "apps/web/app/strategy/page.tsx",
        "apps/web/app/capital-allocation/page.tsx",
        "apps/web/app/sales-cockpit/page.tsx",
        "apps/web/app/deal-desk/page.tsx",
        "apps/web/app/approvals/page.tsx",
        "apps/web/app/workers/page.tsx",
        "apps/web/app/trust/page.tsx",
        "apps/web/app/ai-governance/page.tsx",
        "apps/web/app/finance/page.tsx",
        "apps/web/app/finance-ops/page.tsx",
        "apps/web/app/distribution/page.tsx",
        "apps/web/app/launch/page.tsx",
        "apps/web/app/market-attack/page.tsx",
        "apps/web/app/campaigns/page.tsx",
        "apps/web/app/sales-assets/page.tsx",
        "apps/web/app/authority/page.tsx",
        "apps/web/app/revenue-intelligence/page.tsx",
        "apps/web/app/moat/page.tsx",
        "apps/web/app/playbooks/page.tsx",
        "apps/web/app/proof-library/page.tsx",
        "apps/web/app/partner-ecosystem/page.tsx",
        "apps/web/app/productization/page.tsx",
        "apps/web/app/customer-success/page.tsx",
        "apps/web/app/delivery/page.tsx",
        "apps/web/app/retention/page.tsx",
        "apps/web/app/proof/page.tsx",
        "apps/web/app/data/page.tsx",
        "apps/web/app/experiments/page.tsx",
        "apps/web/app/security/page.tsx",
        "apps/web/app/audit/page.tsx",
        "apps/web/app/metrics/page.tsx",
        "apps/web/app/legal/page.tsx",
        "apps/web/app/advisor/page.tsx",
        "apps/web/app/settings/page.tsx",
    ]


def all_generators() -> list[str]:
    return [
        "scripts/generate_ceo_daily_brief.py",
        "scripts/generate_ceo_weekly_review.py",
        "scripts/generate_founder_leverage_report.py",
        "scripts/generate_capital_allocation_report.py",
        "scripts/generate_strategy_scorecard.py",
        "scripts/generate_revenue_forecast.py",
        "scripts/generate_weekly_growth_review.py",
        "scripts/generate_beachhead_sector_scorecard.py",
        "scripts/generate_strategic_account_list.py",
        "scripts/generate_offer_market_fit_report.py",
        "scripts/generate_campaign_command_report.py",
        "scripts/generate_authority_content_queue.py",
        "scripts/generate_partner_pipeline_report.py",
        "scripts/generate_objection_intelligence_report.py",
        "scripts/generate_revenue_intelligence_graph_report.py",
        "scripts/generate_sector_playbook_report.py",
        "scripts/generate_message_performance_report.py",
        "scripts/generate_buyer_objection_graph.py",
        "scripts/generate_proof_library_report.py",
        "scripts/generate_partner_ecosystem_report.py",
        "scripts/generate_productization_pipeline_report.py",
        "scripts/generate_expansion_report.py",
        "scripts/generate_moat_scorecard.py",
        "scripts/generate_ai_governance_board_pack.py",
        "scripts/generate_data_moat_report.py",
        "scripts/generate_talent_gap_report.py",
        "scripts/generate_company_memory_report.py",
        "scripts/generate_monthly_advisor_update.py",
    ]


def docs_indexes() -> list[str]:
    return [
        "docs/ops/INDEX.md",
        "docs/brand/INDEX.md",
        "docs/founder/INDEX.md",
        "docs/strategy/INDEX.md",
        "docs/finance/INDEX.md",
        "docs/people/INDEX.md",
        "docs/positioning/INDEX.md",
        "docs/intelligence/INDEX.md",
        "docs/growth/INDEX.md",
        "docs/launch/INDEX.md",
        "docs/market_attack/INDEX.md",
        "docs/moat/INDEX.md",
        "docs/revenue/INDEX.md",
        "docs/product/INDEX.md",
        "docs/marketing/INDEX.md",
        "docs/ai/INDEX.md",
        "docs/ai_governance/INDEX.md",
        "docs/trust/INDEX.md",
        "docs/evals/INDEX.md",
        "docs/data/INDEX.md",
        "docs/runtime/INDEX.md",
        "docs/delivery/INDEX.md",
        "docs/customer_success/INDEX.md",
        "docs/proof/INDEX.md",
        "docs/partners/INDEX.md",
        "docs/enterprise/INDEX.md",
        "docs/legal/INDEX.md",
        "docs/security/INDEX.md",
        "docs/engineering/INDEX.md",
        "docs/metrics/INDEX.md",
        "docs/learning/INDEX.md",
        "docs/playbooks/INDEX.md",
        "docs/sales_assets/INDEX.md",
    ]


def workflows() -> list[str]:
    return [
        ".github/workflows/dealix-brand-growth-operating-layer.yml",
        ".github/workflows/dealix-company-os.yml",
        ".github/workflows/dealix-execution-launch-layer.yml",
        ".github/workflows/dealix-market-attack-system.yml",
        ".github/workflows/dealix-scale-moat-system.yml",
        ".github/workflows/dealix-founder-management-system.yml",
        ".github/workflows/dealix-hypergrowth-ceo-layer.yml",
        ".github/workflows/dealix-everything.yml",
    ]


def build_checks() -> list[LayerCheck]:
    web_root = REPO_ROOT / "apps" / "web"
    has_node_modules = (web_root / "node_modules" / ".bin" / "next").exists()
    return [
        LayerCheck(
            name="Brand OS",
            kind="script",
            targets=["scripts/verify_brand_system.py"],
        ),
        LayerCheck(
            name="Founder Console (frontend pages)",
            kind="files",
            targets=all_pages(),
        ),
        LayerCheck(
            name="Founder Console (internal API)",
            kind="script",
            targets=["scripts/smoke_internal_api.py"],
        ),
        LayerCheck(
            name="Policy-as-Code",
            kind="script",
            targets=["scripts/verify_policy_as_code.py"],
        ),
        LayerCheck(
            name="Agent Registry",
            kind="script",
            targets=["scripts/verify_agent_registry.py"],
        ),
        LayerCheck(
            name="Machine Registry",
            kind="script",
            targets=["scripts/verify_machine_registry.py"],
        ),
        LayerCheck(
            name="Eval Gate",
            kind="script",
            targets=["scripts/verify_eval_gate.py"],
        ),
        LayerCheck(
            name="Prompt / Output Quality",
            kind="script",
            targets=["scripts/verify_prompt_output_quality.py"],
        ),
        LayerCheck(
            name="AI Governance",
            kind="script",
            targets=["scripts/verify_ai_governance_system.py"],
        ),
        LayerCheck(
            name="Market Attack System",
            kind="script",
            targets=["scripts/verify_market_attack_system.py"],
        ),
        LayerCheck(
            name="Scale / Moat System",
            kind="script",
            targets=["scripts/verify_scale_moat_system.py"],
        ),
        LayerCheck(
            name="Founder Management System",
            kind="script",
            targets=["scripts/verify_founder_management_system.py"],
        ),
        LayerCheck(
            name="Hypergrowth CEO Layer",
            kind="script",
            targets=["scripts/verify_hypergrowth_ceo_layer.py"],
        ),
        LayerCheck(
            name="Founder / CEO Hypergrowth Layer",
            kind="script",
            targets=["scripts/verify_founder_ceo_hypergrowth_layer.py"],
        ),
        LayerCheck(
            name="Launch Readiness",
            kind="script",
            targets=["scripts/verify_launch_readiness.py"],
        ),
        LayerCheck(
            name="Execution / Launch Layer",
            kind="script",
            targets=["scripts/verify_execution_launch_layer.py"],
        ),
        LayerCheck(
            name="Growth System",
            kind="script",
            targets=["scripts/verify_growth_system.py"],
        ),
        LayerCheck(
            name="Marketing System",
            kind="script",
            targets=["scripts/verify_marketing_system.py"],
        ),
        LayerCheck(
            name="Product / Distribution",
            kind="script",
            targets=["scripts/verify_product_distribution.py"],
        ),
        LayerCheck(
            name="Generator scripts",
            kind="files",
            targets=all_generators(),
        ),
        LayerCheck(
            name="Docs scaffolding",
            kind="files",
            targets=docs_indexes(),
        ),
        LayerCheck(
            name="GitHub workflows",
            kind="files",
            targets=workflows(),
        ),
        LayerCheck(
            name="Company OS",
            kind="script",
            targets=["scripts/verify_company_os.py"],
        ),
        LayerCheck(
            name="Frontend build",
            kind="build",
            command=["npm", "--prefix", "apps/web", "run", "build"],
            optional=not has_node_modules,
        ),
    ]


def write_eval_status_csv(results: list[dict]) -> Path:
    out = REPO_ROOT / "evals" / "eval_status.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    is_new = not out.exists()
    fields = ["recorded_at", "layer", "result", "missing_count", "notes"]
    now = datetime.datetime.utcnow().isoformat(timespec="seconds")
    with out.open("a", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        if is_new:
            writer.writeheader()
        for r in results:
            writer.writerow({
                "recorded_at": now,
                "layer": r["name"],
                "result": "PASS" if r["passed"] else "FAIL",
                "missing_count": r["missing_count"],
                "notes": " | ".join(n.replace("\n", " ").replace("\r", " ") for n in r["notes"])[:400],
            })
    return out


def write_human_report(results: list[dict], overall_pass: bool) -> Path:
    out = REPO_ROOT / "docs" / "ops" / "DEALIX_FINAL_READINESS_REPORT.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.datetime.utcnow().isoformat(timespec="seconds")
    lines = [
        "# Dealix Final Readiness Report",
        "",
        f"Generated: {now}",
        "",
        f"## Result: {'PASS' if overall_pass else 'FAIL'}",
        "",
        "## Layers",
        "",
        "| Layer | Result | Missing | Notes |",
        "| --- | --- | --- | --- |",
    ]
    for r in results:
        notes = (" | ".join(r["notes"]) or "—").replace("\n", " ")
        lines.append(f"| {r['name']} | {'PASS' if r['passed'] else 'FAIL'} | {r['missing_count']} | {notes[:200]} |")
    lines += [
        "",
        "## Policy footer",
        "AI prepares · founder approves · no guaranteed claims · no auto external send",
        "",
    ]
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


def write_missing_systems(results: list[dict]) -> Path:
    out = REPO_ROOT / "docs" / "ops" / "DEALIX_MISSING_SYSTEMS.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Dealix Missing Systems", ""]
    any_missing = False
    for r in results:
        if r["passed"]:
            continue
        any_missing = True
        lines.append(f"## {r['name']}")
        if r["missing"]:
            for m in r["missing"]:
                lines.append(f"- missing: `{m}`")
        if r["notes"]:
            for n in r["notes"]:
                lines.append(f"- note: {n[:200]}")
        lines.append("")
    if not any_missing:
        lines.append("_All layers passing._")
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


def main() -> int:
    print("DEALIX EVERYTHING VERIFICATION\n")
    checks = build_checks()
    results: list[dict] = []
    overall_pass = True
    for check in checks:
        passed, notes, missing = check.run()
        if check.optional and not passed and check.kind == "build" and any("not available" in n for n in notes):
            print(f"{check.name}: SKIP (deps not installed) — {notes[0] if notes else ''}")
            results.append({
                "name": check.name,
                "passed": True,
                "notes": notes + ["SKIP (deps not installed)"],
                "missing": missing,
                "missing_count": 0,
            })
            continue
        status = "PASS" if passed else "FAIL"
        print(f"{check.name}: {status}")
        for n in notes:
            for line in n.splitlines()[:2]:
                if line.strip():
                    print(f"  · {line.strip()[:160]}")
        for m in missing[:5]:
            print(f"  · missing: {m}")
        if not passed:
            overall_pass = False
        results.append({
            "name": check.name,
            "passed": passed,
            "notes": notes,
            "missing": missing,
            "missing_count": len(missing),
        })

    report_path = write_human_report(results, overall_pass)
    missing_path = write_missing_systems(results)
    csv_path = write_eval_status_csv(results)

    print()
    print(f"RESULT: {'PASS' if overall_pass else 'FAIL'}")
    print(f"Report: {report_path.relative_to(REPO_ROOT)}")
    print(f"Missing: {missing_path.relative_to(REPO_ROOT)}")
    print(f"Eval status: {csv_path.relative_to(REPO_ROOT)}")
    json_summary = {
        "result": "PASS" if overall_pass else "FAIL",
        "layers": [
            {"name": r["name"], "passed": r["passed"], "missing_count": r["missing_count"]}
            for r in results
        ],
    }
    if os.environ.get("DEALIX_VERIFY_JSON"):
        print()
        print(json.dumps(json_summary, indent=2))
    return 0 if overall_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
