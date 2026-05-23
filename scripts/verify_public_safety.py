"""Public safety guard for the dealix public repo.

Refuses to let known-private operational artifacts ship in the public tree.
Run locally and in CI before any push to main.
"""
from pathlib import Path

BLOCKED_PATHS = [
    "dashboard_data/company_metrics.json",
    "dashboard_data/revenue_metrics.json",
    "dashboard_data/trust_metrics.json",
    "dashboard_data/delivery_metrics.json",
    "dashboard_data/founder_metrics.json",
]


def main():
    repo_root = Path(__file__).resolve().parent.parent
    found = [p for p in BLOCKED_PATHS if (repo_root / p).exists()]

    if found:
        print("FAIL: private operational artifacts present in public repo:")
        for p in found:
            print("-", p)
        print("Move these to dealix-ops-private or add them to .gitignore.")
        raise SystemExit(1)

    print("PASS: no private operational artifacts in public repo.")


if __name__ == "__main__":
    main()
