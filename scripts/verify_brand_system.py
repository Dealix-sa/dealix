#!/usr/bin/env python3
"""Verify the Dealix brand system surface.

Checks:
- docs/brand/brand-tokens.json exists and contains the required keys.
- apps/web/lib/brand-tokens.ts exists.
- apps/web/components/brand/dealix-logo.tsx exists.
- docs/brand/ contains at least six brand documents.

Exit code 0 on success, 1 on any failure.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import List, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent

BRAND_TOKENS_JSON = REPO_ROOT / "docs" / "brand" / "brand-tokens.json"
BRAND_TOKENS_TS = REPO_ROOT / "apps" / "web" / "lib" / "brand-tokens.ts"
DEALIX_LOGO_TSX = REPO_ROOT / "apps" / "web" / "components" / "brand" / "dealix-logo.tsx"
BRAND_DOCS_DIR = REPO_ROOT / "docs" / "brand"

REQUIRED_TAGLINE = "INTELLIGENT DEALS. REAL GROWTH."
REQUIRED_COLORS = {
    "deepNavy": "#0B1220",
    "emeraldTeal": "#00D1A1",
    "softSilver": "#B2BBC6",
    "slate": "#0F1726",
}
MIN_BRAND_DOCS = 6
REQUIRED_PILLAR_COUNT = 5


def check_brand_tokens_json() -> List[Tuple[str, bool, str]]:
    results: List[Tuple[str, bool, str]] = []
    if not BRAND_TOKENS_JSON.exists():
        return [("brand-tokens.json exists", False, f"missing {BRAND_TOKENS_JSON}")]
    try:
        data = json.loads(BRAND_TOKENS_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [("brand-tokens.json parses", False, f"json error: {exc}")]
    results.append(("brand-tokens.json exists", True, str(BRAND_TOKENS_JSON)))

    tagline = data.get("tagline")
    results.append((
        "tagline matches",
        tagline == REQUIRED_TAGLINE,
        f"got {tagline!r}",
    ))

    colors = data.get("colors", {})
    for key, expected in REQUIRED_COLORS.items():
        actual = colors.get(key)
        results.append((
            f"colors.{key} == {expected}",
            actual == expected,
            f"got {actual!r}",
        ))

    pillars = data.get("pillars", [])
    results.append((
        f"pillars has {REQUIRED_PILLAR_COUNT} entries",
        isinstance(pillars, list) and len(pillars) == REQUIRED_PILLAR_COUNT,
        f"got {len(pillars) if isinstance(pillars, list) else type(pillars).__name__}",
    ))
    return results


def check_file_exists(path: Path, label: str) -> Tuple[str, bool, str]:
    return (label, path.exists(), str(path))


def check_brand_docs_count() -> Tuple[str, bool, str]:
    if not BRAND_DOCS_DIR.exists():
        return (
            f"docs/brand/ has >={MIN_BRAND_DOCS} docs",
            False,
            f"missing directory {BRAND_DOCS_DIR}",
        )
    docs = [p for p in BRAND_DOCS_DIR.glob("*.md") if p.is_file()]
    return (
        f"docs/brand/ has >={MIN_BRAND_DOCS} docs",
        len(docs) >= MIN_BRAND_DOCS,
        f"found {len(docs)}",
    )


def main() -> int:
    results: List[Tuple[str, bool, str]] = []
    results.extend(check_brand_tokens_json())
    results.append(check_file_exists(BRAND_TOKENS_TS, "brand-tokens.ts exists"))
    results.append(check_file_exists(DEALIX_LOGO_TSX, "dealix-logo.tsx exists"))
    results.append(check_brand_docs_count())

    passed = sum(1 for _, ok, _ in results if ok)
    total = len(results)
    print("Dealix brand-system verification")
    print("-" * 40)
    for label, ok, detail in results:
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {label}: {detail}")
    print("-" * 40)
    print(f"summary: {passed}/{total} checks passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
