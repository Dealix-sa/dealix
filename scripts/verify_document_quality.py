"""Verify document quality across canonical Dealix directories.

For every .md inside the listed directories, check:
- has YAML frontmatter (starts with `---` and has a closing `---`).
- has at least 20 lines.
- does not contain banned emoji.
- mentions "Owner" or "Cadence" somewhere.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

DIRS = [
    "docs/trust",
    "docs/revenue",
    "docs/offers/revenue_sprint",
    "docs/delivery/revenue_sprint",
    "docs/learning",
    "docs/dashboard",
    "docs/ai_management",
    "docs/agents",
    "docs/product",
    "docs/finance",
    "docs/client_success",
    "docs/content",
    "docs/partners",
    "docs/people",
]

# Strict directories — must pass every quality check.
# Other directories are considered legacy and produce warnings only.
STRICT_DIRS = {
    "docs/offers/revenue_sprint",
    "docs/delivery/revenue_sprint",
    "docs/people",
    "docs/company_os",
}

# Conservative emoji range: only flag the high-emoji blocks.
EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001F5FF"
    "\U0001F600-\U0001F64F"
    "\U0001F680-\U0001F6FF"
    "\U0001F700-\U0001F77F"
    "\U0001F780-\U0001F7FF"
    "\U0001F900-\U0001F9FF"
    "\U0001FA00-\U0001FA6F"
    "\U0001FA70-\U0001FAFF"
    "\U00002600-\U000026FF"
    "\U00002700-\U000027BF"
    "]"
)


def check_doc(path: Path) -> list[str]:
    rel = path.relative_to(REPO_ROOT).as_posix()
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError) as exc:
        return [f"{rel}: read error {exc!r}"]

    problems: list[str] = []
    lines = text.splitlines()

    # frontmatter
    if not lines or lines[0].strip() != "---":
        problems.append(f"{rel}: no YAML frontmatter")
    else:
        closing = -1
        for i, line in enumerate(lines[1:], start=1):
            if line.strip() == "---":
                closing = i
                break
        if closing < 0:
            problems.append(f"{rel}: unclosed YAML frontmatter")

    # min 20 lines
    if len(lines) < 20:
        problems.append(f"{rel}: only {len(lines)} lines (<20)")

    # emoji
    emojis = EMOJI_RE.findall(text)
    if emojis:
        sample = "".join(emojis[:5])
        problems.append(f"{rel}: contains banned emoji ({sample!r})")

    # Owner or Cadence reference
    low = text.lower()
    if ("owner" not in low) and ("cadence" not in low):
        problems.append(f"{rel}: missing Owner or Cadence section")

    return problems


def main() -> int:
    strict_failures: list[str] = []
    warnings: list[str] = []
    checked = 0
    for d in DIRS:
        base = REPO_ROOT / d
        if not base.exists():
            print(f"SKIP {d} — directory not present")
            continue
        is_strict = d in STRICT_DIRS
        for md in sorted(base.rglob("*.md")):
            checked += 1
            for p in check_doc(md):
                if is_strict:
                    strict_failures.append(p)
                else:
                    warnings.append(p)

    if warnings:
        print("--- warnings (legacy directories, not failing the run) ---")
        for w in warnings[:20]:
            print(f"WARN {w}")
        if len(warnings) > 20:
            print(f"WARN ... and {len(warnings) - 20} more")

    if not strict_failures:
        print(f"\nPASS strict dirs clean ({checked} files checked, {len(warnings)} legacy warnings)")
        print("\nverify_document_quality: PASS")
        return 0

    for f in strict_failures:
        print(f"FAIL {f}")
    print(f"\nverify_document_quality: FAIL ({len(strict_failures)} strict issues, {len(warnings)} warnings, across {checked} files)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
