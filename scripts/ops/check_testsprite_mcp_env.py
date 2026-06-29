#!/usr/bin/env python3
"""Check that TestSprite MCP can be configured without committing secrets.

The script intentionally validates only the presence and shape of the local
`TESTSPRITE_API_KEY` environment variable. It never prints the key value.
"""

from __future__ import annotations

import os
import sys


def main() -> int:
    key = os.getenv("TESTSPRITE_API_KEY", "").strip()

    if not key:
        print("TESTSPRITE_MCP_ENV=MISSING")
        print("Set TESTSPRITE_API_KEY in your local shell, Codespaces secret store, or MCP client config.")
        return 1

    if key.startswith("<") or key.endswith(">"):
        print("TESTSPRITE_MCP_ENV=PLACEHOLDER")
        print("Replace the placeholder with a real key in local secret storage only.")
        return 1

    if len(key) < 20:
        print("TESTSPRITE_MCP_ENV=INVALID")
        print("The key is present but looks too short. The value was not printed.")
        return 1

    print("TESTSPRITE_MCP_ENV=READY")
    print("Secret present. Value intentionally hidden.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
