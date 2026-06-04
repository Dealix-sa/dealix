#!/usr/bin/env python3
"""Static checks for the Dealix website launch (no build required).

Verifies, without running Next.js:
- the expected route page files exist,
- each launch page exports metadata (title + description),
- sitemap.ts and robots.ts exist,
- the three launch CTAs are present,
- all first-5 vertical pages exist,
- no forbidden marketing claims appear in the launch pages.

Writes outputs/site_launch/<date>/site_launch_report.json.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _commercial_common import OUTPUTS_DIR, ROOT, today_str, write_json

WEB = ROOT / "apps" / "web"
APP = WEB / "app"

ROUTE_PAGES = [
    "page.tsx",
    "en/page.tsx",
    "commercial/page.tsx",
    "services/page.tsx",
    "pricing/page.tsx",
    "trust/page.tsx",
    "launch/page.tsx",
    "contact/page.tsx",
    "status/page.tsx",
    "verticals/page.tsx",
    "case-method/page.tsx",
    "media/page.tsx",
    "faq/page.tsx",
]

VERTICAL_SLUGS = [
    "facilities-management",
    "contracting-project-controls",
    "real-estate-property-ops",
    "legal-professional-services",
    "consulting-training-b2b",
]

LAUNCH_PAGES_WITH_METADATA = [
    "en/page.tsx",
    "commercial/page.tsx",
    "services/page.tsx",
    "pricing/page.tsx",
    "trust/page.tsx",
    "launch/page.tsx",
    "contact/page.tsx",
    "verticals/page.tsx",
    "case-method/page.tsx",
    "media/page.tsx",
    "faq/page.tsx",
]

FORBIDDEN_CLAIMS = [
    "guaranteed roi",
    "guaranteed return",
    "100%",
    "replace your team",
    "replace lawyers",
    "automate everything",
    "no human needed",
    "from our database",
    "as discussed",
]

CTA_LABELS = ["Request AI Workflow Audit", "Book Diagnostic", "Start Pilot"]


def run(day: str) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []

    if not APP.exists():
        return {
            "date": day,
            "passed": False,
            "skipped": True,
            "errors": ["apps/web/app not found"],
            "warnings": [],
        }

    # 1. Route page files exist.
    for rel in ROUTE_PAGES:
        if not (APP / rel).exists():
            errors.append(f"missing page: app/{rel}")

    # 2. Vertical pages exist.
    for slug in VERTICAL_SLUGS:
        if not (APP / "verticals" / slug / "page.tsx").exists():
            errors.append(f"missing vertical page: app/verticals/{slug}/page.tsx")

    # 3. Metadata present on launch pages.
    for rel in LAUNCH_PAGES_WITH_METADATA:
        path = APP / rel
        if path.exists():
            text = path.read_text(encoding="utf-8", errors="ignore")
            if "metadata" not in text:
                errors.append(f"no metadata export: app/{rel}")

    # 4. sitemap + robots.
    if not (APP / "sitemap.ts").exists():
        errors.append("missing sitemap.ts")
    if not (APP / "robots.ts").exists():
        errors.append("missing robots.ts")

    # 5. Sitemap references commercial routes.
    sitemap = APP / "sitemap.ts"
    if sitemap.exists():
        stext = sitemap.read_text(encoding="utf-8", errors="ignore")
        for needed in ["/commercial", "/pricing", "/verticals"]:
            if needed not in stext:
                warnings.append(f"sitemap missing route {needed}")

    # 6. CTAs present in shared data.
    data_file = APP / "_launch" / "data.ts"
    if data_file.exists():
        dtext = data_file.read_text(encoding="utf-8", errors="ignore")
        for label in CTA_LABELS:
            if label not in dtext:
                errors.append(f"missing CTA label: {label}")
        for slug in VERTICAL_SLUGS:
            if slug not in dtext:
                errors.append(f"vertical not in data: {slug}")
    else:
        errors.append("missing app/_launch/data.ts")

    # 7. Forbidden claims scan over launch pages + shared content.
    scan_targets = [APP / rel for rel in ROUTE_PAGES if (APP / rel).exists()]
    scan_targets += list((APP / "_launch").glob("*.ts*"))
    scan_targets += [APP / "verticals" / s / "page.tsx" for s in VERTICAL_SLUGS]
    for path in scan_targets:
        if not path.exists():
            continue
        low = path.read_text(encoding="utf-8", errors="ignore").lower()
        for claim in FORBIDDEN_CLAIMS:
            if claim in low:
                errors.append(f"forbidden claim '{claim}' in {path.relative_to(ROOT)}")

    passed = not errors
    return {
        "date": day,
        "passed": passed,
        "skipped": False,
        "pages_checked": len(ROUTE_PAGES) + len(VERTICAL_SLUGS),
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Static website launch checks.")
    parser.add_argument("--date", default=today_str())
    args = parser.parse_args()

    report = run(args.date)
    out = OUTPUTS_DIR / "site_launch" / args.date / "site_launch_report.json"
    write_json(out, report)

    if report.get("skipped"):
        print("SITE LAUNCH CHECK: SKIPPED (no web app).")
        return 0
    if report["passed"]:
        print(
            f"SITE LAUNCH CHECK: PASS — {report['pages_checked']} pages, "
            f"{len(report['warnings'])} warnings."
        )
        return 0
    print("SITE LAUNCH CHECK: FAIL", file=sys.stderr)
    for e in report["errors"]:
        print(f"  - {e}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
