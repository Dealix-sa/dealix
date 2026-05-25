"""Verify the Dealix 24/7 Growth Factory scaffolding is in place."""

from __future__ import annotations

from pathlib import Path


REQUIRED = [
    "docs/ops/DEALIX_24_7_GROWTH_FACTORY.md",
    "docs/acquisition/LEAD_SCALE_TARGETS.md",
    "docs/acquisition/MULTI_CHANNEL_OUTREACH_SYSTEM.md",
    "docs/control_plane/APPROVAL_DASHBOARD_SYSTEM.md",
    "docs/acquisition/SECTOR_MACHINES.md",
    "docs/founder/CEO_15_MINUTE_CONTROL_ROUTINE.md",
    "docs/acquisition/OUTREACH_THROUGHPUT_RULES.md",
    "docs/acquisition/SUPPRESSION_LIST_SYSTEM.md",
    "docs/acquisition/GROWTH_FACTORY_METRICS.md",
    "schemas/lead_intelligence_base.schema.json",
    "scripts/run_growth_hourly.py",
    "scripts/run_growth_4h.py",
    "scripts/run_growth_daily.py",
    "deploy/cron/dealix_crontab.example",
    "deploy/SERVER_DEPLOYMENT_CHECKLIST.md",
    "machines/README.md",
]


def main() -> int:
    failures: list[str] = []
    for file in REQUIRED:
        p = Path(file)
        if not p.exists():
            failures.append(f"Missing: {file}")
        elif p.stat().st_size < 50:
            failures.append(f"Too short: {file}")
    if failures:
        print("24/7 Growth Factory verification failed:")
        for failure in failures:
            print("-", failure)
        return 1
    print("PASS: 24/7 Growth Factory is ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
