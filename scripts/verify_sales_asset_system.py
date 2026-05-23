#!/usr/bin/env python3
"""Verify the Sales Asset Factory contract.

Exits 0 on success, 1 on hard failure. Warnings are non-fatal.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from market_attack_common import (  # type: ignore[import-not-found]
    BANNED_PHRASES,
    BOOTSTRAP_ROOT,
    REPO_ROOT,
    load_with_fallback,
    private_ops_root,
)

REQUIRED_DIRS = (
    REPO_ROOT / "assets" / "sales" / "one_pagers",
    REPO_ROOT / "assets" / "sales" / "proposals",
    REPO_ROOT / "assets" / "sales" / "samples",
    REPO_ROOT / "assets" / "sales" / "objections",
    REPO_ROOT / "assets" / "sales" / "proof_safe",
)

REQUIRED_DOCS = (
    REPO_ROOT / "docs" / "sales_assets" / "SALES_ASSET_FACTORY.md",
    REPO_ROOT / "docs" / "sales_assets" / "SAMPLE_ASSET_SYSTEM.md",
    REPO_ROOT / "docs" / "sales_assets" / "PROPOSAL_ASSET_SYSTEM.md",
    REPO_ROOT / "docs" / "sales_assets" / "SECTOR_ONE_PAGER_SYSTEM.md",
    REPO_ROOT / "docs" / "sales_assets" / "OBJECTION_RESPONSE_LIBRARY.md",
    REPO_ROOT / "docs" / "sales_assets" / "PROOF_SAFE_ASSET_POLICY.md",
)

ASSET_CSV_HEADERS = [
    "asset_id",
    "type",
    "sector",
    "offer",
    "title",
    "status",
    "approval_status",
    "proof_status",
    "risk_level",
    "file_path",
    "next_action",
]


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []

    for d in REQUIRED_DIRS:
        if not d.is_dir():
            failures.append(f"missing directory: {d}")

    for doc in REQUIRED_DOCS:
        if not doc.is_file():
            failures.append(f"missing doc: {doc}")

    priv = private_ops_root()
    primary = priv / "sales_assets" / "sales_asset_registry.csv"
    bootstrap = BOOTSTRAP_ROOT / "sales_assets" / "sales_asset_registry.csv"
    headers, rows, source = load_with_fallback(primary, bootstrap)
    if source == "fallback":
        warnings.append(
            f"sales_asset_registry: using bootstrap template ({bootstrap})."
        )
    if headers and headers != ASSET_CSV_HEADERS:
        failures.append(
            f"sales_asset_registry.csv headers mismatch. "
            f"got: {headers} expected: {ASSET_CSV_HEADERS}"
        )

    for r in rows:
        status = (r.get("status") or "").strip()
        approval = (r.get("approval_status") or "").strip()
        proof = (r.get("proof_status") or "").strip()
        if status == "approved" and proof == "evidence_required":
            warnings.append(
                f"asset {r.get('asset_id','?')} is approved but proof_status=evidence_required."
            )
        if status not in ("draft", "review", "approved", "champion", "retired"):
            warnings.append(
                f"asset {r.get('asset_id','?')} has unknown status '{status}'."
            )
        path_str = (r.get("file_path") or "").strip()
        if status in ("approved", "champion") and path_str:
            full = REPO_ROOT / path_str
            if not full.is_file():
                warnings.append(
                    f"asset {r.get('asset_id','?')} file missing: {path_str}"
                )

    # Lint markdown docs for banned phrases. Doctrine docs (which list the
    # banned phrases as policy) are skipped via the same allowlist used by
    # verify_prompt_output_quality.py.
    for doc in REQUIRED_DOCS:
        if not doc.is_file():
            continue
        text = doc.read_text(encoding="utf-8").lower()
        is_doctrine_doc = (
            "banned" in text
            or "we never" in text
            or "we do not promise" in text
            or "banned phrases" in text
        )
        if is_doctrine_doc:
            continue
        for phrase in BANNED_PHRASES:
            if phrase in text:
                warnings.append(f"{doc}: contains '{phrase}'")
                break

    print("Sales Asset System Verification")
    print("=" * 50)
    if failures:
        print("FAILURES:")
        for f in failures:
            print(f"  - {f}")
    else:
        print("FAILURES: none")
    print()
    if warnings:
        print("WARNINGS:")
        for w in warnings:
            print(f"  - {w}")
    else:
        print("WARNINGS: none")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
