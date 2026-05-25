"""Dealix operations CLI.

Lightweight command-line entry points that point the operator at the right
files in the **private** operations workspace. The CLI never writes client
data into the public repository; it only ensures the private workspace exists
and prints the canonical file paths to use.
"""

from __future__ import annotations

__all__ = ["commands"]
