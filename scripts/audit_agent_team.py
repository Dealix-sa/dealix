#!/usr/bin/env python3
"""Audit the Dealix agent team registry and governance surface.

This is a dependency-free (stdlib-only) auditor so it can run in the
minimal `agent-team-audit` workflow without installing the full app.

It answers the questions the founder asks about the agent fleet:
  - Which agent surfaces exist and are non-empty?
  - Are the Claude (`.md`) and Codex (`.toml`) sub-agents in parity?
  - Does every Claude sub-agent declare the required frontmatter?
  - Do all governance docs exist (registry, contract, matrix, ...)?
  - Are the 11-non-negotiable doctrine guard tests present?

Outputs:
  - reports/agents/agent_team_audit.json
  - reports/agents/agent_team_audit.md
  - stdout line: ``DEALIX_AGENT_TEAM_AUDIT=PASS|FAIL``

Exit code is 0 by default (report-only). Pass ``--strict`` to exit 1 when
the verdict is FAIL — this is what CI uses so the audit can gate a PR.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Agent surfaces that must exist and be non-empty for a governed fleet.
AGENT_DIRS: tuple[str, ...] = (
    ".claude/agents",          # Claude Code sub-agents (markdown)
    ".codex/agents",           # Codex sub-agents (toml mirror)
    ".cursor/rules",           # Cursor operating rules
    "core/agents",             # internal agent runtime (base + multi-agent)
    "autonomous_growth/agents",  # autonomous growth agent swarm
    "auto_client_acquisition",   # deterministic execution planes the agents call
    "mcp_server",              # MCP tool surface (read-only business OS)
    "prompts",                 # canonical operator prompts
)

# Governance docs that must exist for the agent team to count as governed.
REQUIRED_DOCS: tuple[str, ...] = (
    "AGENTS.md",
    "docs/agents/AGENT_TEAM_REGISTRY.md",
    "docs/agents/AGENT_OUTPUT_CONTRACT.md",
    "docs/agents/AGENT_PERMISSION_MATRIX.md",
    "docs/agents/AGENT_DAILY_RUNBOOK.md",
    "docs/agents/AGENT_SECURITY_POLICY.md",
    "docs/agents/TOKEN_BUDGET_POLICY.md",
    "docs/agents/PR_TRIAGE_POLICY.md",
)

# Docs that are good to have but do not fail the audit when missing.
RECOMMENDED_DOCS: tuple[str, ...] = (
    "docs/agents/README.md",
    "docs/ops/FOUNDER_DAILY_OPERATING_RHYTHM.md",
    "docs/ops/FOUNDER_AGENT_PLAYBOOK_AR.md",
)

CLAUDE_AGENT_DIR = ".claude/agents"
CODEX_AGENT_DIR = ".codex/agents"

# Frontmatter keys every Claude sub-agent must declare (identity = doctrine #9).
REQUIRED_CLAUDE_FRONTMATTER: tuple[str, ...] = ("name", "description", "tools")

# At least this many doctrine guard tests must exist (the 11 non-negotiables).
MIN_DOCTRINE_GUARD_TESTS = 5


def _exists(rel: str) -> bool:
    return (ROOT / rel).exists()


def _count_files(rel: str) -> int:
    path = ROOT / rel
    if not path.exists():
        return 0
    if path.is_file():
        return 1
    return sum(1 for child in path.rglob("*") if child.is_file())


def _frontmatter_block(text: str) -> str | None:
    """Return the YAML frontmatter block between the first two ``---`` fences."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            return "\n".join(lines[1:idx])
    return None


def _claude_agent_names() -> list[str]:
    directory = ROOT / CLAUDE_AGENT_DIR
    if not directory.exists():
        return []
    return sorted(p.stem for p in directory.glob("*.md"))


def _codex_agent_names() -> list[str]:
    directory = ROOT / CODEX_AGENT_DIR
    if not directory.exists():
        return []
    return sorted(p.stem for p in directory.glob("*.toml"))


def _check_frontmatter() -> dict[str, dict[str, object]]:
    directory = ROOT / CLAUDE_AGENT_DIR
    result: dict[str, dict[str, object]] = {}
    if not directory.exists():
        return result
    for path in sorted(directory.glob("*.md")):
        block = _frontmatter_block(path.read_text(encoding="utf-8"))
        if block is None:
            result[path.stem] = {"ok": False, "missing": list(REQUIRED_CLAUDE_FRONTMATTER)}
            continue
        present = {
            line.split(":", 1)[0].strip()
            for line in block.splitlines()
            if ":" in line and not line.startswith((" ", "\t"))
        }
        missing = [key for key in REQUIRED_CLAUDE_FRONTMATTER if key not in present]
        result[path.stem] = {"ok": not missing, "missing": missing}
    return result


def _doctrine_guard_tests() -> list[str]:
    tests_dir = ROOT / "tests"
    if not tests_dir.exists():
        return []
    return sorted(p.name for p in tests_dir.glob("test_no_*.py"))


def build_report() -> dict:
    """Build the audit report dictionary. Pure (no I/O side effects)."""
    gaps: list[str] = []
    warnings: list[str] = []

    surfaces: dict[str, dict[str, object]] = {}
    for rel in AGENT_DIRS:
        count = _count_files(rel)
        surfaces[rel] = {"exists": _exists(rel), "files": count}
        if count == 0:
            gaps.append(f"Missing or empty agent surface: {rel}")

    required_docs = {doc: _exists(doc) for doc in REQUIRED_DOCS}
    for doc, ok in required_docs.items():
        if not ok:
            gaps.append(f"Missing required governance doc: {doc}")

    recommended_docs = {doc: _exists(doc) for doc in RECOMMENDED_DOCS}
    for doc, ok in recommended_docs.items():
        if not ok:
            warnings.append(f"Missing recommended doc: {doc}")

    claude_agents = _claude_agent_names()
    codex_agents = _codex_agent_names()
    claude_only = sorted(set(claude_agents) - set(codex_agents))
    codex_only = sorted(set(codex_agents) - set(claude_agents))
    parity_in_sync = not claude_only and not codex_only
    if claude_only:
        warnings.append(f"Claude agents without a Codex mirror: {', '.join(claude_only)}")
    if codex_only:
        warnings.append(f"Codex agents without a Claude mirror: {', '.join(codex_only)}")

    frontmatter = _check_frontmatter()
    for name, info in frontmatter.items():
        if not info["ok"]:
            missing = ", ".join(info["missing"])  # type: ignore[arg-type]
            gaps.append(f"Claude agent '{name}' missing frontmatter: {missing}")

    doctrine_tests = _doctrine_guard_tests()
    doctrine_ok = len(doctrine_tests) >= MIN_DOCTRINE_GUARD_TESTS
    if not doctrine_ok:
        gaps.append(
            f"Only {len(doctrine_tests)} doctrine guard tests found "
            f"(expected >= {MIN_DOCTRINE_GUARD_TESTS})"
        )

    verdict = "FAIL" if gaps else "PASS"

    return {
        "schema": "dealix.agent_team_audit/v1",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "verdict": verdict,
        "agent_surfaces": surfaces,
        "claude_agents": claude_agents,
        "codex_agents": codex_agents,
        "registry_parity": {
            "in_sync": parity_in_sync,
            "claude_only": claude_only,
            "codex_only": codex_only,
        },
        "agent_frontmatter": frontmatter,
        "required_docs": required_docs,
        "recommended_docs": recommended_docs,
        "doctrine_guard_tests": {
            "count": len(doctrine_tests),
            "ok": doctrine_ok,
            "tests": doctrine_tests,
        },
        "gaps": gaps,
        "warnings": warnings,
    }


def render_markdown(report: dict) -> str:
    lines: list[str] = ["# Dealix Agent Team Audit", ""]
    lines.append(f"- Verdict: **{report['verdict']}**")
    lines.append(f"- Generated: `{report['generated_at_utc']}`")
    lines.append(f"- Claude agents: {len(report['claude_agents'])} · "
                 f"Codex agents: {len(report['codex_agents'])} · "
                 f"Registry parity: {'in sync' if report['registry_parity']['in_sync'] else 'OUT OF SYNC'}")
    lines.append("")

    lines.append("## Agent surfaces")
    for rel, info in report["agent_surfaces"].items():
        mark = "✅" if info["files"] else "❌"
        lines.append(f"- {mark} `{rel}`: {info['files']} files")
    lines.append("")

    lines.append("## Sub-agent roster")
    for name in report["claude_agents"]:
        fm = report["agent_frontmatter"].get(name, {})
        mark = "✅" if fm.get("ok") else "❌"
        mirror = "↔ codex" if name in report["codex_agents"] else "⚠ no codex mirror"
        lines.append(f"- {mark} `{name}` ({mirror})")
    lines.append("")

    lines.append("## Required governance docs")
    for doc, ok in report["required_docs"].items():
        lines.append(f"- {'✅' if ok else '❌'} `{doc}`")
    lines.append("")

    doctrine = report["doctrine_guard_tests"]
    lines.append(f"## Doctrine guard tests ({doctrine['count']})")
    lines.append(f"- {'✅' if doctrine['ok'] else '❌'} "
                 f"{doctrine['count']} `tests/test_no_*.py` guards present")
    lines.append("")

    lines.append("## Gaps (fail the audit)")
    if report["gaps"]:
        lines.extend(f"- ❌ {gap}" for gap in report["gaps"])
    else:
        lines.append("- None")
    lines.append("")

    lines.append("## Warnings (non-blocking)")
    if report["warnings"]:
        lines.extend(f"- ⚠ {warning}" for warning in report["warnings"])
    else:
        lines.append("- None")
    lines.append("")

    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit the Dealix agent team.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 when the verdict is FAIL (used by CI to gate a PR).",
    )
    parser.add_argument(
        "--json-only",
        action="store_true",
        help="Print the JSON report to stdout instead of the verdict line.",
    )
    args = parser.parse_args(argv)

    report = build_report()

    out_dir = ROOT / "reports" / "agents"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "agent_team_audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (out_dir / "agent_team_audit.md").write_text(
        render_markdown(report), encoding="utf-8"
    )

    if args.json_only:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for gap in report["gaps"]:
            print(f"GAP: {gap}", file=sys.stderr)
        for warning in report["warnings"]:
            print(f"WARN: {warning}", file=sys.stderr)
        print(f"DEALIX_AGENT_TEAM_AUDIT={report['verdict']}")

    if args.strict and report["verdict"] == "FAIL":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
