#!/usr/bin/env python3
"""Static (no-browser) inspection of the apps/web website for launch.

Checks page presence, SEO metadata, sitemap/robots, and the absence of
exaggerated marketing claims. Does NOT run a browser or build — purely reads
files so it works in any CI runner.

Writes outputs/final_launch_control/site_static_check.json.
Exit 0 on PASS, 1 on FAIL (critical checks only).

Usage:
    python scripts/site_launch_static_check.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from launch_os import paths  # noqa: E402
from launch_os.compliance import find_forbidden_claims, SITE_FORBIDDEN_CLAIMS  # noqa: E402
from launch_os.verify import Check, summarize, print_checks  # noqa: E402

WEB = paths.REPO_ROOT / "apps" / "web"
APP = WEB / "app"

# Core pages: homepage is critical; the rest are reported as warnings if absent.
CRITICAL_PAGES = ("page.tsx",)  # homepage
EXPECTED_PAGES = (
    "ar",
    "status",
    "safety",
    "go-to-market",
    "revenue-os",
    "value-engine",
)


def run() -> dict:
    checks: list[Check] = []
    if not WEB.exists():
        checks.append(Check("apps_web_present", False, critical=False, detail="no apps/web — site check skipped"))
        return summarize(checks)

    checks.append(Check("apps_web_present", True, critical=False))

    # Homepage (critical).
    homepage = APP / "page.tsx"
    checks.append(Check("homepage_present", homepage.exists(), detail=paths.rel(homepage)))

    # Expected pages (warnings).
    for name in EXPECTED_PAGES:
        d = APP / name
        present = (d / "page.tsx").exists() or (d.with_suffix(".tsx")).exists() or d.exists()
        checks.append(Check(f"page_{name}", present, critical=False))

    # SEO metadata + sitemap + robots (critical for a public launch).
    layout = APP / "layout.tsx"
    layout_text = layout.read_text(encoding="utf-8", errors="ignore") if layout.exists() else ""
    checks.append(Check("metadata_present", "export const metadata" in layout_text, detail=paths.rel(layout)))
    checks.append(Check("openGraph_present", "openGraph" in layout_text, critical=False))
    checks.append(Check("sitemap_present", (APP / "sitemap.ts").exists() or (APP / "sitemap.xml").exists()))
    checks.append(Check("robots_present", (APP / "robots.ts").exists() or (APP / "robots.txt").exists()))
    checks.append(Check("manifest_present", (APP / "manifest.ts").exists(), critical=False))

    # Forbidden claims scan across all tsx/ts/md content under apps/web/app.
    offenders: list[str] = []
    scanned = 0
    for p in APP.rglob("*"):
        if p.suffix in (".tsx", ".ts", ".mdx", ".md") and p.is_file():
            scanned += 1
            hits = find_forbidden_claims(p.read_text(encoding="utf-8", errors="ignore"), SITE_FORBIDDEN_CLAIMS)
            if hits:
                offenders.append(f"{paths.rel(p)}: {hits}")
    checks.append(
        Check(
            "no_forbidden_claims",
            len(offenders) == 0,
            detail=f"offenders={offenders[:5]}" if offenders else f"scanned={scanned} files",
        )
    )

    # Arabic + English presence (RTL launch requirement).
    has_ar = (APP / "ar").exists()
    checks.append(Check("arabic_route_present", has_ar, critical=False))

    return summarize(checks)


def main() -> int:
    paths.ensure_dirs()
    result = run()
    out = paths.FINAL_CONTROL_OUT / "site_static_check.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print_checks("site", [Check(**c) for c in result["checks"]])
    print(f"[site] wrote {paths.rel(out)}")
    print("[site] PASS" if result["pass"] else "[site] FAIL")
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
