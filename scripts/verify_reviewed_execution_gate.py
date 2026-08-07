"""Verify Dealix reviewed-execution agent and skill acceptance invariants."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEWER = ROOT / ".codex" / "agents" / "dealix-fresh-reviewer.toml"
SKILL = ROOT / ".agents" / "skills" / "dealix" / "reviewed-execution" / "SKILL.md"
README = ROOT / ".agents" / "skills" / "dealix" / "README.md"
DOC = ROOT / "docs" / "agents" / "REVIEWED_EXECUTION_GATE.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def verify() -> int:
    errors: list[str] = []

    for path in (REVIEWER, SKILL, README, DOC):
        if not path.is_file():
            errors.append(f"missing:{path.relative_to(ROOT)}")

    if errors:
        for error in errors:
            print(f"FAIL {error}")
        return 1

    reviewer = _read(REVIEWER)
    skill = _read(SKILL)
    readme = _read(README)
    doc = _read(DOC)

    reviewer_requirements = {
        "read_only_sandbox": 'sandbox_mode = "read-only"',
        "fresh_context": "fresh context",
        "no_self_fix": "implement the fixes you discover",
        "ship_verdict": "`ship`",
        "fix_first_verdict": "`fix-first`",
        "rethink_verdict": "`rethink`",
        "runtime_unverified": "unverified",
    }
    for name, needle in reviewer_requirements.items():
        if needle.lower() not in reviewer.lower():
            errors.append(f"reviewer_missing:{name}")

    skill_requirements = {
        "bounded_contract": "Task Contract",
        "existing_agents": "Existing agents to reuse",
        "non_overlapping": "non-overlapping",
        "parent_diff": "git diff <base_sha>...HEAD",
        "fresh_reviewer": "dealix-fresh-reviewer",
        "review_receipt": "REVIEW_RECEIPT",
        "merge_separate": "Merge remains a separate gate",
        "cycle_limit": "two",
    }
    for name, needle in skill_requirements.items():
        if needle.lower() not in skill.lower():
            errors.append(f"skill_missing:{name}")

    if "dealix-reviewed-execution" not in readme:
        errors.append("readme_missing:dealix-reviewed-execution")

    doc_requirements = (
        "DannyMac180/sol-advisor",
        "Adoption matrix",
        "Parallel agents",
        "Auto-merge",
        "Review Receipt",
    )
    for needle in doc_requirements:
        if needle.lower() not in doc.lower():
            errors.append(f"doc_missing:{needle}")

    forbidden_skill_patterns = (
        "auto-merge on reviewer `ship`",
        "unlimited agent swarm",
    )
    for pattern in forbidden_skill_patterns:
        if pattern.lower() not in skill.lower():
            errors.append(f"skill_missing_anti_pattern:{pattern}")

    if errors:
        for error in errors:
            print(f"FAIL {error}")
        return 1

    print("PASS reviewed_execution_gate")
    return 0


if __name__ == "__main__":
    raise SystemExit(verify())
