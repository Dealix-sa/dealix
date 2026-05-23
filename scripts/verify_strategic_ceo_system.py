"""Verify that Dealix Strategic CEO System v3 files are present and substantive."""
from pathlib import Path

REQUIRED = [
    "DEALIX_CEO_SYSTEM_INDEX.md",
    "docs/strategy/STRATEGIC_PORTFOLIO_SYSTEM.md",
    "docs/founder/COMPANY_RISK_REGISTER.md",
    "docs/founder/FOUNDER_LEVERAGE_SYSTEM.md",
    "docs/revenue/REVENUE_PUSH_PACK.md",
    "docs/delivery/DELIVERY_RESCUE_PACK.md",
    "docs/trust/TRUST_ESCALATION_PACK.md",
    "docs/investor/BOARD_DISCIPLINE.md",
    "docs/ops/SYSTEM_HEALTH_LEVELS.md",
]


def main() -> int:
    failures = []
    for file in REQUIRED:
        p = Path(file)
        if not p.exists():
            failures.append(f"Missing: {file}")
        elif p.stat().st_size < 200:
            failures.append(f"Too short: {file}")
    if failures:
        print("Strategic CEO system verification failed:")
        for f in failures:
            print("-", f)
        return 1
    print("PASS: Strategic CEO system is ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
