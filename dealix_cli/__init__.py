"""Dealix founder CLI.

A small, deliberately boring command set the founder runs every day. The CLI
never sends external messages and never charges customers — it reads private
ops state, runs verifiers, and prepares drafts.

See `DEALIX_IMPLEMENTATION_AUDIT.md` for the full list of commands and what
each verifies.
"""

__all__ = ["main"]


def main() -> None:
    from dealix_cli.__main__ import main as _main

    _main()
