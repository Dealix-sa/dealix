#!/usr/bin/env python3
"""Verify the Data Room OS (V9). Static, read-only, artifact-only."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import v9_lib  # noqa: E402

REQUIRED_FILES = [
    "docs/data-room-os/00_DATA_ROOM_OS.md",
    "docs/data-room-os/01_DATA_ROOM_INDEX.md",
    "docs/data-room-os/02_COMPANY_FOLDER_STRUCTURE.md",
    "docs/data-room-os/03_INVESTOR_PACKET.md",
    "docs/data-room-os/04_ENTERPRISE_CLIENT_PACKET.md",
    "docs/data-room-os/05_PARTNER_PACKET.md",
    "docs/data-room-os/06_DUE_DILIGENCE_QA.md",
    "docs/data-room-os/07_EVIDENCE_POLICY.md",
    "docs/data-room-os/99_DATA_ROOM_REPORT.md",
]


def verify() -> dict:
    return v9_lib.run_system_check("data_room", REQUIRED_FILES)


def main() -> int:
    return v9_lib.print_and_exit(verify())


if __name__ == "__main__":
    raise SystemExit(main())
