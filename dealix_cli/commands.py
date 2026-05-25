"""Dealix CLI command implementations.

These commands act on the *private* operations workspace, which is a sibling
repository or directory (typically ``dealix-ops-private``). The path is
provided by the operator via ``--private-ops`` (or the ``PRIVATE_OPS``
environment variable in the Makefile). The public repository never stores
client-identifying data.
"""

from __future__ import annotations

from pathlib import Path

PRIVATE_SUBDIRS = (
    "clients",
    "clients/_template",
    "delivery",
    "client_success",
    "learning",
)


def ensure_private_ops(private_ops: str | Path) -> Path:
    """Ensure the private ops workspace exists with the canonical subdirs.

    Returns the resolved Path to the workspace. Does not create or copy any
    client data — only the directory skeleton.
    """
    path = Path(private_ops).expanduser().resolve()
    path.mkdir(parents=True, exist_ok=True)
    for sub in PRIVATE_SUBDIRS:
        (path / sub).mkdir(parents=True, exist_ok=True)
    return path


def delivery(private_ops: str) -> None:
    """Show the canonical files an operator should touch during delivery."""
    private_ops_path = ensure_private_ops(private_ops)
    print()
    print("Dealix Delivery & Client Success")
    print("=" * 40)
    print("Private ops workspace:")
    print(f"  {private_ops_path}")
    print()
    print("Use these files:")
    print(f"- {private_ops_path / 'clients/_template/client_os.md'}")
    print(f"- {private_ops_path / 'clients/_template/intake.md'}")
    print(f"- {private_ops_path / 'clients/_template/delivery_report.md'}")
    print(f"- {private_ops_path / 'clients/_template/qa_checklist.md'}")
    print(f"- {private_ops_path / 'clients/_template/handoff.md'}")
    print(f"- {private_ops_path / 'clients/_template/feedback.md'}")
    print(f"- {private_ops_path / 'clients/_template/health_score.md'}")
    print(f"- {private_ops_path / 'client_success/retention_tracker.csv'}")
    print()
    print("Delivery Rule:")
    print(
        "No delivery without intake, QA, handoff, feedback request, "
        "and next action."
    )
