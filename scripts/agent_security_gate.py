#!/usr/bin/env python3
"""Agent Security Gate — scan workflows + agent configs for risky patterns.

Targets the agentic-CI attack surface: untrusted text (issue/PR/comment bodies)
flowing into ``run:``/``with:`` steps, over-broad write permissions, and
checkout of untrusted PR head code under ``pull_request_target`` (which runs
with repository secrets). Deterministic, dependency-light, exits non-zero on
any finding so CI can block the PR.

Usage:
    python scripts/agent_security_gate.py [--root .github/workflows] [--json]
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Events that carry attacker-controllable content into the workflow context.
_UNTRUSTED_EVENTS = (
    "issue_comment",
    "issues",
    "pull_request_target",
    "pull_request_review",
    "pull_request_review_comment",
    "discussion",
    "discussion_comment",
)

# An expression that reads attacker-controllable text from the event payload.
_UNTRUSTED_EXPR = re.compile(
    r"\$\{\{[^}]*github\.event[^}]*\."
    r"(?:body|title|head_ref|label|name|login|comment)\b[^}]*\}\}",
    re.IGNORECASE,
)
_HEAD_CHECKOUT = re.compile(
    r"ref:\s*\$\{\{\s*github\.event\.pull_request\.head\.(?:sha|ref)\s*\}\}",
    re.IGNORECASE,
)


def _step_lines_using(text: str, pattern: re.Pattern[str]) -> list[int]:
    """Line numbers where an untrusted expression appears in a run:/with:/env: context."""
    hits: list[int] = []
    block_indent: int | None = None
    key_re = re.compile(r"-?\s*(?:run|with|env)\s*:")
    for i, raw in enumerate(text.splitlines(), start=1):
        if not raw.strip():
            continue
        indent = len(raw) - len(raw.lstrip())
        if key_re.match(raw.strip()):
            if pattern.search(raw):  # inline value on the key line (e.g. "- run: echo X")
                hits.append(i)
            block_indent = indent
            continue
        if block_indent is not None:
            if indent > block_indent:
                if pattern.search(raw):  # nested value inside the block
                    hits.append(i)
            else:
                block_indent = None
    return hits


def _triggers(text: str) -> set[str]:
    found: set[str] = set()
    for event in _UNTRUSTED_EVENTS:
        if re.search(rf"^\s*{re.escape(event)}\s*:", text, re.MULTILINE) or re.search(
            rf"\b{re.escape(event)}\b", text.split("jobs:", 1)[0] if "jobs:" in text else text
        ):
            found.add(event)
    return found


def scan_workflow(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    findings: list[str] = []
    rel = path.name

    if re.search(r"permissions:\s*write-all", text):
        findings.append(f"{rel}: permissions: write-all (use least-privilege contents: read)")

    untrusted = _triggers(text)
    if untrusted:
        for ln in _step_lines_using(text, _UNTRUSTED_EXPR):
            findings.append(
                f"{rel}:{ln}: untrusted event text flows into a run/with/env step "
                f"(injection risk; triggers: {sorted(untrusted)})"
            )
        if "pull_request_target" in untrusted and _HEAD_CHECKOUT.search(text):
            findings.append(
                f"{rel}: pull_request_target checks out PR head code while secrets are available"
            )
    return findings


def scan(root: Path) -> list[str]:
    findings: list[str] = []
    for path in sorted(root.glob("*.yml")) + sorted(root.glob("*.yaml")):
        findings.extend(scan_workflow(path))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT / ".github" / "workflows")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    findings = scan(args.root)
    if args.json:
        print(
            json.dumps({"findings": findings, "count": len(findings)}, ensure_ascii=False, indent=2)
        )
    elif findings:
        print("Agent Security Gate — findings:")
        for f in findings:
            print(f"  - {f}")
    else:
        print("Agent Security Gate: no risky patterns found.")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
