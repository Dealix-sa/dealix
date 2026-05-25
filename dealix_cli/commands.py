"""Founder-facing CLI commands.

Every command in this module is read-only: it points the founder at the
private-ops files and operating rules they need to review. Nothing here
sends external messages, mutates state, or hits the network.
"""

from __future__ import annotations

from pathlib import Path


def ensure_private_ops(private_ops: str | Path) -> Path:
    """Return an absolute path to the private-ops root, creating it if missing.

    Sub-folders used by the people/partner OS (``founder/``, ``people/``,
    ``partners/``) are created on demand so the printed checklist always
    references real directories.
    """

    root = Path(private_ops).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    for sub in ("founder", "people", "partners"):
        (root / sub).mkdir(parents=True, exist_ok=True)
    return root


def people(private_ops: str | Path) -> None:
    """Print the People & Delegation review checklist."""

    private_ops_path = ensure_private_ops(private_ops)
    print("\nDealix People & Delegation")
    print("=" * 40)
    print("Review these private files:")
    print(f"- {private_ops_path / 'founder' / 'founder_bottleneck_log.csv'}")
    print(f"- {private_ops_path / 'people' / 'delegation_log.csv'}")
    print(f"- {private_ops_path / 'people' / 'contractor_tracker.csv'}")
    print(f"- {private_ops_path / 'people' / 'access_log.csv'}")
    print(f"- {private_ops_path / 'founder' / 'personal_leverage_dashboard.md'}")
    print("\nPeople Rule:")
    print("Do not delegate unclear work. Document, template, QA, then delegate.")


def partners(private_ops: str | Path) -> None:
    """Print the Partners review checklist."""

    private_ops_path = ensure_private_ops(private_ops)
    print("\nDealix Partners")
    print("=" * 40)
    print("Review these private files:")
    print(f"- {private_ops_path / 'partners' / 'partner_pipeline.csv'}")
    print(f"- {private_ops_path / 'partners' / 'partner_tracker.csv'}")
    print("\nPartner Rule:")
    print(
        "Partners can refer. Partners cannot promise, discount, change scope, "
        "or publish proof."
    )
