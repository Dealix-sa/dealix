"""Dealix CLI — founder operating commands for the Priority Execution Sprint.

The CLI is a thin wrapper around the founder's daily / weekly / sprint
checklists.  It expects the operator to keep a private operations repo
checked out alongside this one (default path: `../dealix-ops-private`).

Public surfaces:
    python -m dealix_cli sprint     --private-ops ../dealix-ops-private
    python -m dealix_cli daily      --private-ops ../dealix-ops-private
    python -m dealix_cli close-day  --private-ops ../dealix-ops-private
    python -m dealix_cli weekly     --private-ops ../dealix-ops-private
    python -m dealix_cli verify     --private-ops ../dealix-ops-private
    python -m dealix_cli dashboard  --private-ops ../dealix-ops-private
"""

__all__ = ["commands"]
