"""Verify Strategic Opportunity OS and Hermes Agents repository assets.

This script is intentionally lightweight and has no third-party dependencies.
It checks that the strategy and Hermes documentation packs exist and that
pyproject.toml exposes the optional tooling extras used by the packs.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "docs/strategic-opportunity-os/README.md",
    "docs/strategic-opportunity-os/01-strategic-opportunity-map.md",
    "docs/strategic-opportunity-os/02-opportunity-scoring-model.md",
    "docs/strategic-opportunity-os/03-tooling-adoption-matrix.md",
    "docs/strategic-opportunity-os/04-ai-data-capability-roadmap.md",
    "docs/strategic-opportunity-os/05-product-bet-portfolio.md",
    "docs/strategic-opportunity-os/06-gtm-expansion-playbook.md",
    "docs/strategic-opportunity-os/07-founder-100-day-execution-plan.md",
    "docs/strategic-opportunity-os/08-review-plan.md",
    "docs/hermes-agents/README.md",
    "docs/hermes-agents/01-agent-charters.md",
    "docs/hermes-agents/02-governance-and-controls.md",
    "docs/hermes-agents/03-operations-cadence.md",
    "docs/hermes-agents/04-escalation-matrix.md",
    "hermes_agents/__init__.py",
    "hermes_agents/registry.py",
    "hermes_agents/policy.py",
    "hermes_agents/cli.py",
]

REQUIRED_EXTRAS = [
    "observability",
    "evaluation",
    "data_quality",
    "analytics",
    "security_advanced",
    "automation",
    "agents",
    "founder_stack",
]

REQUIRED_PYPROJECT_SNIPPETS = [
    'hermes-agents = "hermes_agents.cli:main"',
    '"hermes_agents*"',
]


def main() -> int:
    missing_files = [path for path in REQUIRED_FILES if not (ROOT / path).exists()]

    pyproject_path = ROOT / "pyproject.toml"
    pyproject = pyproject_path.read_text(encoding="utf-8") if pyproject_path.exists() else ""
    missing_extras = [extra for extra in REQUIRED_EXTRAS if f"{extra} = [" not in pyproject]
    missing_snippets = [snippet for snippet in REQUIRED_PYPROJECT_SNIPPETS if snippet not in pyproject]

    if missing_files or missing_extras or missing_snippets:
        if missing_files:
            print("Missing Strategic Opportunity OS or Hermes files:")
            for path in missing_files:
                print(f"- {path}")
        if missing_extras:
            print("Missing optional dependency extras:")
            for extra in missing_extras:
                print(f"- {extra}")
        if missing_snippets:
            print("Missing pyproject snippets:")
            for snippet in missing_snippets:
                print(f"- {snippet}")
        return 1

    print("Strategic Opportunity OS and Hermes Agents verification passed.")
    print(f"Checked {len(REQUIRED_FILES)} files and {len(REQUIRED_EXTRAS)} optional extras.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
