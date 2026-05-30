#!/usr/bin/env python3
"""Export the FastAPI OpenAPI schema for contract review.

The script imports `api.main:app` and writes the current OpenAPI document to
`docs/architecture/openapi.json` by default. It is intentionally small and
side-effect-light so CI can use it as an API contract smoke check.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from api.main import app

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "docs" / "architecture" / "openapi.json"


def export_openapi(output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    schema = app.openapi()
    output.write_text(
        json.dumps(schema, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    # `output` may be a scratch path outside the repo (e.g. the contract check
    # writes to a TemporaryDirectory under /tmp); fall back to the absolute path
    # rather than crashing on relative_to.
    try:
        display: Path = output.relative_to(ROOT)
    except ValueError:
        display = output
    print(f"Exported OpenAPI schema to {display}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Export Dealix OpenAPI schema")
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output JSON path (default: docs/architecture/openapi.json)",
    )
    args = parser.parse_args()
    export_openapi(args.output if args.output.is_absolute() else ROOT / args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
