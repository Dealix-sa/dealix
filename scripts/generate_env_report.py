#!/usr/bin/env python3
"""Generate a deterministic env coverage report.

Never prints values. Reports which env vars are set, by category.
Output: reports/health/env-report-YYYY-MM-DD.md
"""

from __future__ import annotations

import datetime as _dt
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "reports" / "health"

CATEGORIES = {
    "Database / auth": ["DATABASE_URL", "JWT_SECRET_KEY", "DEALIX_ADMIN_PASSWORD", "DEALIX_ADMIN_TOKEN"],
    "AI providers": ["OPENAI_API_KEY", "MINIMAX_API_KEY", "KIMI_API_KEY", "DEEPSEEK_API_KEY", "OPENROUTER_API_KEY", "AI_PROVIDER_DEFAULT", "AI_MODE_DEMO"],
    "Payment providers (stubs)": ["MOYASAR_SECRET_KEY", "STRIPE_SECRET_KEY"],
    "Frontend": ["NEXT_PUBLIC_DEMO_MODE", "NEXT_PUBLIC_BASE_URL"],
    "Observability": ["SENTRY_DSN", "DATADOG_API_KEY"],
}


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    date = _dt.date.today().isoformat()
    lines = [f"# Env coverage report — {date}", "", "_Values are never printed; only presence/absence._", ""]
    for label, keys in CATEGORIES.items():
        lines.append(f"## {label}")
        lines.append("")
        for k in keys:
            state = "SET" if os.environ.get(k) else "—"
            lines.append(f"- `{k}`: {state}")
        lines.append("")
    out = OUT_DIR / f"env-report-{date}.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
