#!/usr/bin/env python3
"""
Launch bundle validator — verifies schemas, file counts, and JSON validity.

Run: python scripts/launch/launch_bundle_validate.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

SCHEMA_DIR = REPO_ROOT / "schemas" / "launch"
DOCS_DIRS = {
    "strategy": REPO_ROOT / "docs" / "strategy",
    "offers": REPO_ROOT / "docs" / "offers",
    "targeting": REPO_ROOT / "docs" / "targeting",
    "sales": REPO_ROOT / "docs" / "sales",
    "proposal": REPO_ROOT / "docs" / "proposal",
    "content": REPO_ROOT / "docs" / "content",
    "delivery": REPO_ROOT / "docs" / "delivery",
    "trust": REPO_ROOT / "docs" / "trust",
}
EVAL_DIR = REPO_ROOT / "evals" / "launch"
REPORT_DIR = REPO_ROOT / "reports" / "launch"

PASS = "✅"
FAIL = "❌"
WARN = "⚠️"


def validate_schemas() -> list[str]:
    errors = []
    if not SCHEMA_DIR.exists():
        errors.append(f"{FAIL} schemas/launch/ does not exist")
        return errors
    schema_files = list(SCHEMA_DIR.glob("*.json"))
    print(f"\n📋 Schemas ({len(schema_files)} files):")
    for sf in sorted(schema_files):
        try:
            data = json.loads(sf.read_text(encoding="utf-8"))
            schema_id = data.get("$id", "no $id")
            print(f"  {PASS} {sf.name} — {schema_id}")
        except json.JSONDecodeError as e:
            errors.append(f"{FAIL} {sf.name}: invalid JSON — {e}")
            print(f"  {FAIL} {sf.name}: invalid JSON — {e}")
    return errors


def validate_docs() -> list[str]:
    errors = []
    print("\n📚 Docs:")
    for category, path in DOCS_DIRS.items():
        if not path.exists():
            print(f"  {WARN} docs/{category}/ not found — skipping")
            continue
        files = list(path.glob("*.md"))
        arabic_files = [f for f in files if "_AR" in f.name or "AR.md" in f.name]
        print(f"  {PASS} docs/{category}/: {len(files)} files ({len(arabic_files)} Arabic)")
    return errors


def validate_evals() -> list[str]:
    errors = []
    if not EVAL_DIR.exists():
        errors.append(f"{WARN} evals/launch/ not found")
        return errors
    eval_files = list(EVAL_DIR.glob("*.yaml"))
    print(f"\n🧪 Evals ({len(eval_files)} files):")
    for ef in sorted(eval_files):
        content = ef.read_text(encoding="utf-8")
        case_count = content.count("  - id:")
        print(f"  {PASS} {ef.name}: {case_count} cases")
    return errors


def validate_python_modules() -> list[str]:
    errors = []
    print("\n🐍 Python modules:")
    modules = [
        "dealix.launch_os.icp_scorer",
        "dealix.launch_os.vertical_scorer",
        "dealix.launch_os.trust_preflight",
        "dealix.launch_os.outreach_factory",
        "dealix.launch_os.proposal_engine",
        "dealix.launch_os.pipeline_tracker",
        "dealix.launch_os.founder_daily_command",
    ]
    for mod in modules:
        try:
            __import__(mod)
            print(f"  {PASS} {mod}")
        except ImportError as e:
            errors.append(f"{FAIL} {mod}: {e}")
            print(f"  {FAIL} {mod}: {e}")
    return errors


def print_summary(all_errors: list[str]) -> None:
    print("\n" + "=" * 60)
    if all_errors:
        print(f"RESULT: {FAIL} {len(all_errors)} issue(s) found")
        for err in all_errors:
            print(f"  {err}")
        sys.exit(1)
    else:
        print(f"RESULT: {PASS} Launch bundle validation passed")


def main() -> None:
    print("=" * 60)
    print("DEALIX LAUNCH BUNDLE VALIDATOR")
    print("=" * 60)

    all_errors: list[str] = []
    all_errors += validate_schemas()
    all_errors += validate_docs()
    all_errors += validate_evals()
    all_errors += validate_python_modules()
    print_summary(all_errors)


if __name__ == "__main__":
    main()
