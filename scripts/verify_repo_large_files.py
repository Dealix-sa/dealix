#!/usr/bin/env python3
"""
verify_repo_large_files.py

Prevent accidentally committing large archives/binaries that bloat the repo
or contain secrets. Warns if any tracked file in the top-level tree exceeds
50 MB or if forbidden archive extensions appear in git-tracked files.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SIZE_LIMIT_MB = 50
FORBIDDEN_EXTENSIONS = {".zip", ".tar", ".tar.xz", ".tar.gz", ".rar", ".7z", ".iso", ".dmg", ".exe"}

# These archives are already in git history on main. They are tracked as a
# known baseline; no new archives should be added. They should be moved to
# git-lfs or release artifacts in a future cleanup.
TRACKED_ARCHIVE_BASELINE = {
    "DEALIX_FULL_SESSION_EXPORT.zip",
    "DEALIX_Market_Launch_Bundle_v1.zip",
    "Dealix. Files .zip",
    "Kimi_Agent_تنفيذ شامل.zip",
    "OKComputer_GitHub_طلب_v9.zip",
    "dealix_kimi_clean_merge_pack.zip",
    "dealix_market_domination_pack_v12_part1_core_repo.tar.xz",
    "dealix_market_domination_pack_v12_part2_archive_history.tar.xz",
    "dealix_market_domination_pack_v4.zip",
    "dealix_website_brand_company_min_patch.zip",
}


def list_tracked_files() -> list[str]:
    try:
        out = subprocess.check_output(
            ["git", "ls-tree", "-r", "--name-only", "HEAD"],
            cwd=REPO_ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        )
        return [l for l in out.splitlines() if l.strip()]
    except Exception:
        return []


def main() -> int:
    print("Repository Large File Check")
    print("=" * 50)
    tracked = list_tracked_files()
    if not tracked:
        print("⚠️  Could not list tracked files (not a git repo or no HEAD).")
        return 0

    errors: list[str] = []
    for rel in tracked:
        basename = Path(rel).name
        if Path(rel).suffix.lower() in FORBIDDEN_EXTENSIONS:
            if basename in TRACKED_ARCHIVE_BASELINE:
                continue
            errors.append(f"Forbidden archive tracked: {rel}")
        path = REPO_ROOT / rel
        if path.exists():
            size_mb = path.stat().st_size / (1024 * 1024)
            if size_mb > SIZE_LIMIT_MB:
                errors.append(f"Oversized file tracked: {rel} ({size_mb:.1f} MB)")

    if errors:
        print("❌ Found issues:")
        for e in errors:
            print(f"   - {e}")
        return 1

    print("✅ No forbidden archives or oversized tracked files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
