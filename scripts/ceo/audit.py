"""Run the Dealix trust / overclaim / PII audit.

Exits non-zero if any violation is found. Used in CI and by `make audit`.

Scans:
  - Forbidden / overclaim phrases (see docs/trust/NO_OVERCLAIM_POLICY.md)
  - PII-shaped strings (emails, Saudi phone numbers, national ID shapes)

By default the audit scopes to the CEO Operating System surface — the
directories and files the founder/CEO layer owns. Pass --all to scan
everything under docs/. The CI gate uses the default scope.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"


FORBIDDEN_PHRASES: tuple[str, ...] = (
    "guaranteed revenue",
    "guaranteed leads",
    "guarantee revenue",
    "guarantee leads",
    "guaranteed roi",
    "best in saudi arabia",
    "best in mena",
    "best in the world",
    "100% accurate",
    "zero human work",
    "fully autonomous",
    "ai-powered platform",
)

PII_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}", re.IGNORECASE),
    re.compile(r"(?<!\d)\+?9665\d{8}(?!\d)"),
    re.compile(r"(?<!\d)05\d{8}(?!\d)"),
    re.compile(r"(?<!\d)[12]\d{9}(?!\d)"),
)


PII_EXCEPTIONS: tuple[str, ...] = (
    "founder@example.com",
    "sami@dealix",
    "claude.ai/code",
)


SCAN_EXCLUDE_DIRS: frozenset[str] = frozenset(
    {
        "node_modules",
        ".git",
        "_deprecated",
    }
)


CEO_OS_SCOPES: tuple[str, ...] = (
    "founder",
    "strategy/NORTH_STAR.md",
    "strategy/STRATEGIC_THESIS.md",
    "strategy/ICP_STRATEGY.md",
    "strategy/GTM_STRATEGY.md",
    "strategy/GROWTH_MODEL.md",
    "strategy/MOAT_SYSTEM.md",
    "strategy/MONTHLY_MOAT_REVIEW.md",
    "strategy/COMPETITIVE_STRATEGY.md",
    "strategy/STRATEGY_INDEX.md",
    "revenue/REVENUE_COMMAND_CENTER.md",
    "revenue/REVENUE_CONTROL_SYSTEM.md",
    "revenue/REVENUE_MODEL.md",
    "revenue/OFFER_LADDER.md",
    "revenue/PIPELINE_STAGES.md",
    "revenue/CASH_RULES.md",
    "revenue/BAD_REVENUE_FILTER.md",
    "revenue/OFFER_EVOLUTION_SYSTEM.md",
    "revenue/REVENUE_METRICS.md",
    "sales/FOUNDER_DM_PACK.md",
    "sales/FOUNDER_SALES_CALL_ONE_PAGER.md",
    "sales/PROPOSAL_FAST_TEMPLATE.md",
    "sales/PROPOSAL_FOLLOWUP_RULE.md",
    "sales/OBJECTIONS_LOG.md",
    "trust",
    "finance",
    "ai_management",
    "client_success",
    "product/PRODUCTIZATION_COMMAND_CENTER.md",
    "product/PRODUCTIZATION_ENGINE.md",
    "product/FEATURE_INTAKE.md",
    "product/BUILD_DEFER_KILL.md",
    "product/NO_OVERBUILD_POLICY.md",
    "product/DORA_METRICS_POLICY.md",
    "product/ENGINEERING_HEALTH_REVIEW.md",
    "product/ROADMAP.md",
    "content/CONTENT_COMMAND_CENTER.md",
    "content/CONTENT_STRATEGY.md",
    "content/FOUNDER_VOICE.md",
    "content/LINKEDIN_SYSTEM.md",
    "content/X_SYSTEM.md",
    "content/CASE_STUDY_SYSTEM.md",
    "content/PROOF_LIBRARY.md",
    "people",
    "partners/PARTNER_COMMAND_CENTER.md",
    "partners/PARTNER_STRATEGY.md",
    "partners/REFERRAL_TERMS.md",
    "partners/PARTNER_SCORECARD.md",
    "delivery/revenue_sprint",
)


@dataclass(frozen=True)
class Finding:
    path: Path
    line_no: int
    kind: str
    detail: str


def iter_markdown_files(roots: list[Path]):
    seen: set[Path] = set()
    for root in roots:
        if root.is_file() and root.suffix == ".md":
            if root not in seen:
                seen.add(root)
                yield root
            continue
        if not root.exists():
            continue
        for path in root.rglob("*.md"):
            if any(part in SCAN_EXCLUDE_DIRS for part in path.parts):
                continue
            if path in seen:
                continue
            seen.add(path)
            yield path


def scan_doctrine(file_path: Path) -> list[Finding]:
    findings: list[Finding] = []
    text = file_path.read_text(encoding="utf-8", errors="ignore")
    lower = text.lower()

    name = file_path.name.lower()
    if any(
        marker in name
        for marker in (
            "no_overclaim_policy",
            "safe_language_library",
            "objections_log",
            "incident_response",
            "ai_threat_model",
            "ai_risk_register",
        )
    ):
        return findings

    for phrase in FORBIDDEN_PHRASES:
        idx = lower.find(phrase)
        if idx == -1:
            continue
        line_no = lower.count("\n", 0, idx) + 1
        findings.append(
            Finding(file_path, line_no, "doctrine", f"forbidden phrase: '{phrase}'")
        )
    return findings


def scan_pii(file_path: Path) -> list[Finding]:
    findings: list[Finding] = []
    if "case_study" in file_path.name.lower():
        return findings
    text = file_path.read_text(encoding="utf-8", errors="ignore")
    for line_no, line in enumerate(text.splitlines(), start=1):
        for pattern in PII_PATTERNS:
            for m in pattern.finditer(line):
                hit = m.group(0)
                if any(exc in hit.lower() for exc in PII_EXCEPTIONS):
                    continue
                findings.append(
                    Finding(file_path, line_no, "pii", f"PII-shaped string: '{hit}'")
                )
    return findings


def resolve_roots(scope_all: bool) -> list[Path]:
    if scope_all:
        return [DOCS]
    roots: list[Path] = []
    for rel in CEO_OS_SCOPES:
        roots.append(DOCS / rel)
    return roots


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--all",
        action="store_true",
        help="Scan everything under docs/, not just the CEO OS surface.",
    )
    args = parser.parse_args()

    roots = resolve_roots(args.all)
    scope_label = "all of docs/" if args.all else "CEO OS surface"

    findings: list[Finding] = []
    for md in iter_markdown_files(roots):
        findings.extend(scan_doctrine(md))
        findings.extend(scan_pii(md))

    if findings:
        print(f"[audit] {len(findings)} finding(s) in {scope_label}:")
        for f in findings:
            rel = f.path.relative_to(ROOT)
            print(f"  {f.kind:8s}  {rel}:{f.line_no}  {f.detail}")
        return 1

    print(f"[audit] no doctrine or PII violations found in {scope_label}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
