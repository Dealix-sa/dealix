#!/usr/bin/env python3
"""Generate a local `.mcp.json` for TestSprite without committing secrets.

Usage:
    export TESTSPRITE_API_KEY="..."
    python scripts/ops/prepare_testsprite_mcp_local.py

The generated `.mcp.json` is ignored by Git and must stay local-only.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / ".mcp.json"


def main() -> int:
    key = os.getenv("TESTSPRITE_API_KEY", "").strip()
    if not key:
        print("TESTSPRITE_MCP_CONFIG=MISSING_SECRET")
        print("Set TESTSPRITE_API_KEY first. The key will not be printed.")
        return 1

    config = {
        "mcpServers": {
            "TestSprite": {
                "command": "npx",
                "args": ["@testsprite/testsprite-mcp@latest"],
                "env": {"API_KEY": key},
            }
        }
    }

    OUT.write_text(json.dumps(config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("TESTSPRITE_MCP_CONFIG=WRITTEN")
    print("Wrote local-only .mcp.json. Secret value intentionally hidden.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
