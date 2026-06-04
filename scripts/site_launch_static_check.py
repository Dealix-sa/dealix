#!/usr/bin/env python3
"""
Dealix Website Static Launch Check (no browser).

Statically inspects apps/web (if present) for:
  - presence of key pages
  - presence of SEO metadata / sitemap / robots where applicable
  - absence of forbidden / exaggerated marketing claims

Writes outputs/final_launch_control/site_static_check.json.
Exit 0 if no critical failures (or apps/web absent), 1 otherwise.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
WEB = REPO / "apps" / "web"
OUT = REPO / "outputs" / "final_launch_control" / "site_static_check.json"

FORBIDDEN_CLAIMS = [
    "guaranteed roi",
    "100% guaranteed",
    "replace your team",
    "automate everything",
    "no human needed",
]


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    if not WEB.exists():
        result = {
            "checked_at": datetime.now(timezone.utc).isoformat(),
            "web_present": False,
            "pass": True,
            "note": "apps/web not present — site check skipped (non-critical).",
        }
        OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
        print("[site-static] apps/web absent — skipped (PASS)")
        return 0

    app = WEB / "app"
    pages = {p.name for p in app.iterdir()} if app.exists() else set()
    has_home = (app / "page.tsx").exists()
    has_layout = (app / "layout.tsx").exists()
    has_status = (app / "status").exists()

    # SEO signals
    layout_txt = (app / "layout.tsx").read_text(encoding="utf-8", errors="ignore") if has_layout else ""
    has_metadata = "metadata" in layout_txt or bool(
        list(app.rglob("*.tsx")) and any(
            "metadata" in f.read_text(encoding="utf-8", errors="ignore").lower()
            for f in list(app.rglob("*.tsx"))[:80]
        )
    )
    public = WEB / "public"
    has_robots = (public / "robots.txt").exists() or (app / "robots.ts").exists()
    has_sitemap = (public / "sitemap.xml").exists() or (app / "sitemap.ts").exists()

    # Forbidden claim scan across source
    violations = []
    for f in list(app.rglob("*.tsx")) + list(app.rglob("*.ts")):
        low = f.read_text(encoding="utf-8", errors="ignore").lower()
        for claim in FORBIDDEN_CLAIMS:
            if claim in low:
                violations.append({"file": str(f.relative_to(REPO)), "claim": claim})

    checks = {
        "homepage": has_home,
        "layout": has_layout,
        "status_page": has_status,
        "seo_metadata": bool(has_metadata),
        "robots": bool(has_robots),
        "sitemap": bool(has_sitemap),
        "no_forbidden_claims": len(violations) == 0,
    }
    # Critical: homepage + layout + no forbidden claims. SEO/robots/sitemap advisory.
    critical = checks["homepage"] and checks["layout"] and checks["no_forbidden_claims"]

    result = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "web_present": True,
        "pages_found": sorted(pages),
        "checks": checks,
        "claim_violations": violations[:20],
        "pass": critical,
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[site-static] {'PASS' if critical else 'FAIL'} — pages={len(pages)}")
    for k, v in checks.items():
        print(f"  - {k}: {v}")
    return 0 if critical else 1


if __name__ == "__main__":
    raise SystemExit(main())
