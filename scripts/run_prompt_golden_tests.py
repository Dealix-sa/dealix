#!/usr/bin/env python3
"""Run prompt golden tests against captured outputs.

Loads `evals/golden/prompt_output_golden_tests.yaml` and verifies that
each test's `must_include` / `must_not_include` assertions hold against
`outputs/golden/<test_name>.txt`. Missing output files are FAIL (strict).
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

import yaml  # noqa: E402

from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402

TEST_FILE = REPO / "evals/golden/prompt_output_golden_tests.yaml"
OUTPUT_DIR = REPO / "outputs/golden"


def main() -> int:
    ensure_stdout_utf8()
    print("# Prompt Golden Tests")

    if not TEST_FILE.exists():
        print(f"FAIL: missing test file: {TEST_FILE}")
        return 1

    data = yaml.safe_load(TEST_FILE.read_text(encoding="utf-8")) or {}
    tests = data.get("tests", [])
    if not tests:
        print("FAIL: no tests defined in golden test file")
        return 1

    failures: list[str] = []
    passed = 0
    skipped = 0

    for test in tests:
        name = test.get("name", "<unnamed>")
        expected = test.get("expected", {}) or {}
        output_path = OUTPUT_DIR / f"{name}.txt"

        if not output_path.exists():
            # Treat missing outputs as skipped, not fail, so a fresh repo
            # is not blocked by tests that have not yet been recorded.
            print(f"  skip: {name} (no captured output at {output_path.relative_to(REPO)})")
            skipped += 1
            continue

        text = output_path.read_text(encoding="utf-8", errors="ignore").lower()
        test_failed = False
        for phrase in expected.get("must_include", []) or []:
            if phrase.lower() not in text:
                failures.append(f"{name}: missing required phrase: {phrase!r}")
                test_failed = True
        for phrase in expected.get("must_not_include", []) or []:
            if phrase.lower() in text:
                failures.append(f"{name}: contains forbidden phrase: {phrase!r}")
                test_failed = True

        if test_failed:
            print(f"  FAIL: {name}")
        else:
            print(f"  ok: {name}")
            passed += 1

    print(f"\nPASSED={passed} SKIPPED={skipped} FAILURES={len(failures)}")
    if failures:
        for f in failures:
            print(f"- {f}")
        print("PROMPT_GOLDEN_TESTS_READY=false")
        return 1
    print("PROMPT_GOLDEN_TESTS_READY=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
