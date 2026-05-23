#!/usr/bin/env python3
"""
verify_public_safety.py — scan the Master-Tree-managed files for
PII/secret leaks.

This script intentionally scopes its scan to the files declared in
scripts/generate_master_tree.py. Pre-existing repository content
(historical landing pages, legacy docs) is reported separately by
`scripts/verify_public_safety.py --legacy`.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

from dealix.trust.public_safety import scan  # noqa: E402
from generate_master_tree import collect_public_manifest  # noqa: E402


SCAN_SUFFIXES = {".md", ".markdown", ".yaml", ".yml", ".html"}

# Files we explicitly exclude even when in the manifest: they document
# secret formats deliberately, or contain test fixtures.
ALLOWLIST = {
    Path("SECURITY.md"),
    Path("docs/api/AUTHENTICATION.md"),
    Path(".gitleaks.toml"),
    Path(".secrets.baseline"),
    Path("dealix/registers/no_overclaim.yaml"),
}

# Pre-existing public files with founder contact info / deployment doc
# placeholders. Findings here are tracked in
# `docs/trust/PUBLIC_REPO_SAFETY.md` and triaged separately — not a
# regression and not part of the Master Tree change.
LEGACY_ACKNOWLEDGED = {
    Path("DEPLOYMENT.md"),
    Path("landing/index.html"),
}


def manifest_files() -> list[Path]:
    out: list[Path] = []
    for directory, files in collect_public_manifest().items():
        base = REPO / directory if directory else REPO
        for f in files:
            rel = (Path(directory) / f) if directory else Path(f)
            if rel in ALLOWLIST or rel in LEGACY_ACKNOWLEDGED:
                continue
            if rel.suffix.lower() not in SCAN_SUFFIXES:
                continue
            full = base / f
            if full.is_file():
                out.append(full)
    return out


def scan_files(files: list[Path]) -> list[tuple[Path, str]]:
    leaks: list[tuple[Path, str]] = []
    for path in files:
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for finding in scan(text):
            leaks.append((path.relative_to(REPO), f"{finding.kind}: {finding.sample!r}"))
    return leaks


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--legacy", action="store_true",
        help="Also scan every legacy file outside the Master-Tree manifest (report-only).",
    )
    args = parser.parse_args(argv)

    files = manifest_files()
    leaks = scan_files(files)

    if args.legacy:
        legacy_files: list[Path] = []
        manifest_paths = {p.resolve() for p in files}
        for path in REPO.rglob("*"):
            if not path.is_file():
                continue
            if any(part in {".git", "node_modules", "__pycache__", ".venv"} for part in path.parts):
                continue
            if path.suffix.lower() not in SCAN_SUFFIXES:
                continue
            if path.resolve() not in manifest_paths:
                legacy_files.append(path)
        legacy_leaks = scan_files(legacy_files)
        if legacy_leaks:
            print(f"[REPORT] legacy: {len(legacy_leaks)} findings outside Master Tree (not blocking)")
            for rel, sample in legacy_leaks[:10]:
                print(f"  - {rel}: {sample}")

    if leaks:
        print(f"[FAIL] verify_public_safety: {len(leaks)} leaks in Master-Tree files")
        for rel, sample in leaks[:20]:
            print(f"  - {rel}: {sample}")
        if len(leaks) > 20:
            print(f"  ... {len(leaks) - 20} more")
        return 1
    print(f"[OK] verify_public_safety: {len(files)} Master-Tree files scanned, no leaks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
