#!/usr/bin/env python3
"""
audit_local_artifacts.py — honestly categorize a parallel local dealix working copy
against the canonical GitHub repo, before bulk-uploading anything.

Why this exists
---------------
A prior session produced many files on a Windows machine (e.g. dealix-1) that were
never pushed to GitHub. Some are legitimate assets (HTML one-pagers, brand assets,
PDFs, presentations, Markdown strategy docs). Others are theatrical Python stubs
(e.g. a "100-engine sovereign registry", an "M&A pipeline" that hardcodes
EBITDA multipliers, a "self-healing watchdog" that does nothing measurable). The
stubs would dilute the canonical codebase and, worse, give a false impression that
the platform does things it does not actually do — which is doctrine-violating for
a company whose product is Proof.

This tool has two modes:

1) DIFF MODE (default): walks the local copy, compares to the canonical repo,
   and writes a manifest splitting new/changed files into three buckets:

        KEEP_REAL   - safe, valuable content (sales kit, brand, docs)
        REVIEW      - human must inspect (Python modules, JSON state, configs)
        REJECT_STUB - matches the theatrical-stub heuristic; do not upload

   You then review the manifest and rerun with --emit-copy-script to produce a
   shell/PowerShell script that copies only KEEP_REAL into the canonical repo
   for a real, reviewable commit.

2) SELF-SCAN MODE (--scan-canonical): walks the canonical repo and reports any
   files that match the theatrical-stub heuristic — i.e. theater debt that
   already snuck in. Use this to clean up the canonical repo itself.

This does NOT touch git, does NOT call any remote, and does NOT inject any
evidence into the doctrine ledgers. It only reads files and writes a report.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

KEEP_EXTS = {
    ".md",
    ".html",
    ".htm",
    ".pdf",
    ".pptx",
    ".docx",
    ".png",
    ".jpg",
    ".jpeg",
    ".svg",
    ".webp",
    ".gif",
    ".ico",
    ".csv",
    ".yaml",
    ".yml",
}
REVIEW_EXTS = {".py", ".ts", ".tsx", ".js", ".jsx", ".sh", ".ps1", ".json", ".sql"}

# Path fragments that strongly suggest the file is doctrine-aligned content.
KEEP_PATH_HINTS = (
    "/docs/",
    "/docs\\",
    "/sales-kit/",
    "/sales-kit\\",
    "/brand/",
    "/brand\\",
    "/company/",
    "/company\\",
    "/presentations/",
    "/public/brand",
    "/public\\brand",
    "/marketing/",
    "/marketing\\",
)

# Strong phrases — uniquely identify the prior session's theatrical artefacts.
# A single hit on a STRONG phrase is enough to reject in any mode.
STRONG_STUB_PHRASES = (
    "sovereign_registry",
    "sovereign 100-engine",
    "100-engine sovereign",
    "ultimate_autonomous_vision_2030",
    "execute_50_storm",
    "dealix_self_healing_watchdog",
    "setup_ultimate_cron",
    "dealix_perpetual_engine",
    "autonomous_developer_agent",
    "50-task storm engine",
)

# Weak phrases — appear in legitimate docs/modules too (meta_os is an actual
# directory in this repo; white_label is a real partnership concept). They are
# only flagged in DIFF MODE, where the file is brand new and unknown.
WEAK_STUB_PHRASES = (
    "panic_button",
    "ceo_simulator",
    "investor_room",
    "ebitda_multiplier",
    "treasury split",
    "executive_guard",
)

# Reserved for future contextual rules. The bare number "9090" was tried as a
# contextual flag for "secret passcode", but it produced false positives by
# matching commit-SHA fragments in unrelated docs. Keep empty until a robust
# rule is designed.
CONTEXTUAL_STUB_RULES: tuple[tuple[str, tuple[str, ...]], ...] = ()

# Backwards-compat alias used by older callers/tests.
STUB_PHRASES = STRONG_STUB_PHRASES + WEAK_STUB_PHRASES

# Path fragments that should never be auto-promoted to KEEP_REAL even if the
# extension looks safe (state files that pretend to be evidence).
EVIDENCE_DANGER_PATH_HINTS = (
    "evidence_events_tracker",
    "decision_2026-w",
    "kpi_founder_commercial_import.yaml",
    "founder_pdpl_compliance_pass.yaml",
    "war_room_today.json",
    "founder_briefs/",
    "founder_briefs\\",
)

# Files that legitimately reference the stub heuristic keywords (this tool
# itself, the doctrine doc that names them) and must never be flagged as
# REJECT_STUB. Match is by exact relative path against the local root.
SELF_EXEMPT_PATHS = frozenset(
    {
        "scripts/audit_local_artifacts.py",
        "tests/test_audit_local_artifacts.py",
        "docs/ops/FOUNDER_REALITY_CHECK_AR.md",
    }
)


@dataclass
class FileFinding:
    rel_path: str
    bucket: str
    reason: str
    size_bytes: int
    sha256: str = ""
    stub_hits: list[str] = field(default_factory=list)


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def iter_files(root: Path, ignore_globs: Iterable[str]) -> Iterable[Path]:
    ignore_globs = list(ignore_globs)
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(root).as_posix()
        # Always skip VCS, build artifacts, and node_modules.
        skip_segments = (
            ".git/",
            "node_modules/",
            "__pycache__/",
            ".next/",
            ".venv/",
            "venv/",
            "dist/",
            "build/",
        )
        if any(seg in f"{rel}/" for seg in skip_segments):
            continue
        if any(p.match(g) for g in ignore_globs):
            continue
        yield p


def repo_inventory(repo: Path, ignore_globs: Iterable[str]) -> dict[str, str]:
    inv: dict[str, str] = {}
    for p in iter_files(repo, ignore_globs):
        try:
            inv[p.relative_to(repo).as_posix()] = sha256_of(p)
        except OSError:
            continue
    return inv


def stub_hits_in_text(rel: str, text: str, *, strong_only: bool = False) -> list[str]:
    """Return matching stub phrases.

    When strong_only is True (canonical-scan mode), only STRONG phrases and
    contextual rules whose co-occurrence requirement is met can match. In diff
    mode, WEAK phrases are also considered.
    """
    hay = (rel + "\n" + text).lower()
    hits: list[str] = []
    for phrase in STRONG_STUB_PHRASES:
        if phrase in hay:
            hits.append(phrase)
    if not strong_only:
        for phrase in WEAK_STUB_PHRASES:
            if phrase in hay:
                hits.append(phrase)
    for phrase, required in CONTEXTUAL_STUB_RULES:
        if phrase in hay and any(req in hay for req in required):
            hits.append(phrase)
    return hits


def looks_like_evidence_danger(rel: str) -> bool:
    rel_low = rel.lower()
    return any(hint in rel_low for hint in EVIDENCE_DANGER_PATH_HINTS)


def classify(
    local_root: Path,
    rel: str,
    max_scan_bytes: int = 200_000,
    exempt_paths: frozenset[str] = SELF_EXEMPT_PATHS,
    *,
    canonical_scan: bool = False,
) -> FileFinding:
    full = local_root / rel
    try:
        size = full.stat().st_size
    except OSError:
        size = 0
    suffix = full.suffix.lower()
    rel_norm = "/" + rel.replace("\\", "/")
    rel_posix = rel.replace("\\", "/")

    # Evidence-state files: in DIFF mode never auto-promote them (a fabricated
    # local copy must not overwrite the canonical ledger). In canonical-scan
    # mode they are legitimate by virtue of being committed; skip the guard.
    if not canonical_scan and looks_like_evidence_danger(rel_norm):
        return FileFinding(
            rel_path=rel,
            bucket="REJECT_STUB",
            reason="touches doctrine evidence/KPI ledgers — must not be uploaded by a tool",
            size_bytes=size,
        )

    text_sample = ""
    if suffix in {".py", ".ts", ".tsx", ".js", ".jsx", ".md", ".html", ".htm", ".sh", ".ps1", ".json", ".yaml", ".yml"}:
        try:
            with full.open("rb") as fh:
                text_sample = fh.read(max_scan_bytes).decode("utf-8", errors="replace")
        except OSError:
            text_sample = ""

    hits = stub_hits_in_text(rel, text_sample, strong_only=canonical_scan)

    if hits and rel_posix not in exempt_paths:
        return FileFinding(
            rel_path=rel,
            bucket="REJECT_STUB",
            reason=f"matched theatrical-stub heuristic ({len(hits)} hits)",
            size_bytes=size,
            stub_hits=hits,
        )

    if suffix in KEEP_EXTS and any(hint in rel_norm for hint in KEEP_PATH_HINTS):
        return FileFinding(
            rel_path=rel,
            bucket="KEEP_REAL",
            reason=f"static asset under whitelisted path ({suffix})",
            size_bytes=size,
        )

    if suffix in KEEP_EXTS:
        return FileFinding(
            rel_path=rel,
            bucket="REVIEW",
            reason=f"static asset outside whitelisted paths ({suffix})",
            size_bytes=size,
        )

    if suffix in REVIEW_EXTS:
        return FileFinding(
            rel_path=rel,
            bucket="REVIEW",
            reason=f"code/config file — human review required ({suffix})",
            size_bytes=size,
        )

    return FileFinding(
        rel_path=rel,
        bucket="REVIEW",
        reason=f"unrecognized extension ({suffix or 'none'})",
        size_bytes=size,
    )


def scan_canonical(repo: Path, out_dir: Path, ignore_globs: Iterable[str], exempt: frozenset[str]) -> int:
    """Walk the canonical repo and report any file matching the stub heuristic.

    Returns the number of REJECT_STUB findings (0 means clean).
    """
    print(f"== audit_local_artifacts --scan-canonical ==")
    print(f"  repo: {repo}")
    print(f"  out:  {out_dir}")
    print("  scanning...")
    findings: list[FileFinding] = []
    files_seen = 0
    for p_file in iter_files(repo, ignore_globs):
        files_seen += 1
        rel = p_file.relative_to(repo).as_posix()
        f = classify(repo, rel, exempt_paths=exempt, canonical_scan=True)
        if f.bucket == "REJECT_STUB":
            findings.append(f)
    print(f"    {files_seen:,} files scanned, {len(findings)} stub matches")

    manifest = {
        "mode": "scan-canonical",
        "repo": str(repo),
        "files_scanned": files_seen,
        "stub_findings": [f.__dict__ for f in findings],
    }
    (out_dir / "canonical_scan_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    md_lines: list[str] = []
    md_lines.append("# Canonical repo stub scan\n")
    md_lines.append(f"- repo:           `{repo}`")
    md_lines.append(f"- files scanned:  {files_seen:,}")
    md_lines.append(f"- stub findings:  {len(findings)}\n")
    md_lines.append("## REJECT_STUB findings in canonical repo\n")
    if not findings:
        md_lines.append("_none — canonical repo is clean against the current heuristic._\n")
    else:
        for f in sorted(findings, key=lambda x: x.rel_path):
            extra = f" — hits: {', '.join(f.stub_hits[:3])}" if f.stub_hits else ""
            md_lines.append(f"- `{f.rel_path}` ({f.size_bytes:,} B) — {f.reason}{extra}")
        md_lines.append("")
    (out_dir / "CANONICAL_SCAN_REPORT.md").write_text("\n".join(md_lines), encoding="utf-8")

    print(f"  wrote {out_dir / 'CANONICAL_SCAN_REPORT.md'}")
    print(f"  wrote {out_dir / 'canonical_scan_manifest.json'}")
    return len(findings)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--canonical", required=True, type=Path, help="path to canonical repo clone (this one)")
    p.add_argument("--local", type=Path, help="path to the local working copy to audit (omit when using --scan-canonical)")
    p.add_argument("--scan-canonical", action="store_true", help="scan the canonical repo itself for stub matches; ignores --local")
    p.add_argument("--out", type=Path, default=Path("data/local_artifact_audit"), help="output dir for the audit report and manifest")
    p.add_argument("--ignore", action="append", default=[], help="extra glob patterns to ignore (repeatable)")
    p.add_argument("--exempt", action="append", default=[], help="POSIX-style relative paths to exempt from stub flagging (repeatable; merged with built-in self-exemptions)")
    p.add_argument("--emit-copy-script", action="store_true", help="also emit copy_keep_real.sh and copy_keep_real.ps1 (diff mode only)")
    p.add_argument("--fail-on-stub", action="store_true", help="exit non-zero if any canonical stub findings are reported (CI guard)")
    args = p.parse_args()

    canonical: Path = args.canonical.resolve()
    out_dir: Path = args.out.resolve()

    if not canonical.is_dir():
        print(f"FAIL: canonical path is not a directory: {canonical}", file=sys.stderr)
        return 2

    out_dir.mkdir(parents=True, exist_ok=True)

    exempt = frozenset(SELF_EXEMPT_PATHS | {e.replace("\\", "/") for e in args.exempt})

    if args.scan_canonical:
        n_findings = scan_canonical(canonical, out_dir, args.ignore, exempt)
        if args.fail_on_stub and n_findings > 0:
            print(f"FAIL: {n_findings} stub findings (--fail-on-stub set)", file=sys.stderr)
            return 1
        return 0

    if args.local is None:
        print("FAIL: --local is required in diff mode (or pass --scan-canonical)", file=sys.stderr)
        return 2
    local: Path = args.local.resolve()
    if not local.is_dir():
        print(f"FAIL: local path is not a directory: {local}", file=sys.stderr)
        return 2

    print(f"== audit_local_artifacts ==")
    print(f"  canonical: {canonical}")
    print(f"  local:     {local}")
    print(f"  out:       {out_dir}")

    print("  scanning canonical inventory...")
    canon = repo_inventory(canonical, args.ignore)
    print(f"    {len(canon):,} files")

    findings_new: list[FileFinding] = []
    findings_changed: list[FileFinding] = []
    findings_same = 0

    print("  scanning local copy...")
    for p_local in iter_files(local, args.ignore):
        rel = p_local.relative_to(local).as_posix()
        try:
            digest = sha256_of(p_local)
        except OSError:
            continue
        in_canon = canon.get(rel)
        if in_canon is None:
            f = classify(local, rel, exempt_paths=exempt)
            f.sha256 = digest
            findings_new.append(f)
        elif in_canon != digest:
            f = classify(local, rel, exempt_paths=exempt)
            f.sha256 = digest
            findings_changed.append(f)
        else:
            findings_same += 1

    def by_bucket(findings: list[FileFinding]) -> dict[str, list[FileFinding]]:
        out: dict[str, list[FileFinding]] = {"KEEP_REAL": [], "REVIEW": [], "REJECT_STUB": []}
        for f in findings:
            out[f.bucket].append(f)
        return out

    new_by = by_bucket(findings_new)
    chg_by = by_bucket(findings_changed)

    manifest = {
        "canonical": str(canonical),
        "local": str(local),
        "totals": {
            "canonical_files": len(canon),
            "new": len(findings_new),
            "changed": len(findings_changed),
            "unchanged": findings_same,
        },
        "new": {b: [f.__dict__ for f in fs] for b, fs in new_by.items()},
        "changed": {b: [f.__dict__ for f in fs] for b, fs in chg_by.items()},
    }
    (out_dir / "audit_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    md_lines: list[str] = []
    md_lines.append("# Local artifact audit\n")
    md_lines.append(f"- canonical: `{canonical}`")
    md_lines.append(f"- local:     `{local}`")
    md_lines.append(f"- unchanged: {findings_same:,}")
    md_lines.append(f"- new:       {len(findings_new):,}")
    md_lines.append(f"- changed:   {len(findings_changed):,}\n")

    for label, by in (("New files", new_by), ("Changed files", chg_by)):
        md_lines.append(f"## {label}\n")
        for bucket in ("KEEP_REAL", "REVIEW", "REJECT_STUB"):
            md_lines.append(f"### {bucket} ({len(by[bucket])})")
            if not by[bucket]:
                md_lines.append("_none_\n")
                continue
            for f in sorted(by[bucket], key=lambda x: x.rel_path):
                extra = ""
                if f.stub_hits:
                    extra = f" — hits: {', '.join(f.stub_hits[:3])}"
                md_lines.append(f"- `{f.rel_path}` ({f.size_bytes:,} B) — {f.reason}{extra}")
            md_lines.append("")

    (out_dir / "AUDIT_REPORT.md").write_text("\n".join(md_lines), encoding="utf-8")

    if args.emit_copy_script:
        keep_paths = [f.rel_path for f in findings_new + findings_changed if f.bucket == "KEEP_REAL"]
        sh = ["#!/usr/bin/env bash", "set -euo pipefail", f'LOCAL="{local}"', f'CANON="{canonical}"', ""]
        ps = ["$ErrorActionPreference = 'Stop'", f'$Local = "{local}"', f'$Canon = "{canonical}"', ""]
        for rel in sorted(keep_paths):
            sh.append(f'mkdir -p "$CANON/$(dirname \'{rel}\')"')
            sh.append(f'cp -f "$LOCAL/{rel}" "$CANON/{rel}"')
            win_rel = rel.replace("/", "\\")
            ps.append(f'New-Item -ItemType Directory -Force -Path (Split-Path -Parent "$Canon\\{win_rel}") | Out-Null')
            ps.append(f'Copy-Item -Force "$Local\\{win_rel}" "$Canon\\{win_rel}"')
        (out_dir / "copy_keep_real.sh").write_text("\n".join(sh) + "\n", encoding="utf-8")
        (out_dir / "copy_keep_real.ps1").write_text("\r\n".join(ps) + "\r\n", encoding="utf-8")

    print("")
    print(f"  KEEP_REAL   new: {len(new_by['KEEP_REAL']):>5}   changed: {len(chg_by['KEEP_REAL']):>5}")
    print(f"  REVIEW      new: {len(new_by['REVIEW']):>5}   changed: {len(chg_by['REVIEW']):>5}")
    print(f"  REJECT_STUB new: {len(new_by['REJECT_STUB']):>5}   changed: {len(chg_by['REJECT_STUB']):>5}")
    print("")
    print(f"  wrote {out_dir / 'AUDIT_REPORT.md'}")
    print(f"  wrote {out_dir / 'audit_manifest.json'}")
    if args.emit_copy_script:
        print(f"  wrote {out_dir / 'copy_keep_real.sh'}")
        print(f"  wrote {out_dir / 'copy_keep_real.ps1'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
