"""Shared helpers for Dealix verifier scripts.

A verifier prints PASS / FAIL lines and exits 0 (all pass) or 1 (any fail).
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Verifier:
    def __init__(self, name: str) -> None:
        self.name = name
        self.passes: list[str] = []
        self.failures: list[str] = []

    def check_file(self, rel: str, *, description: str | None = None) -> bool:
        path = ROOT / rel
        label = description or rel
        if path.exists():
            self.passes.append(f"PASS {label}")
            return True
        self.failures.append(f"FAIL {label} -> missing {rel}")
        return False

    def check_dir(self, rel: str, *, description: str | None = None) -> bool:
        path = ROOT / rel
        label = description or rel
        if path.is_dir():
            self.passes.append(f"PASS {label}")
            return True
        self.failures.append(f"FAIL {label} -> missing dir {rel}")
        return False

    def check_files(self, rels: list[str]) -> None:
        for rel in rels:
            self.check_file(rel)

    def check_dirs(self, rels: list[str]) -> None:
        for rel in rels:
            self.check_dir(rel)

    def custom(self, ok: bool, message: str) -> None:
        if ok:
            self.passes.append(f"PASS {message}")
        else:
            self.failures.append(f"FAIL {message}")

    def report(self) -> int:
        print(f"\n[{self.name}] {len(self.passes)} pass / {len(self.failures)} fail")
        for line in self.passes:
            print(f"  {line}")
        for line in self.failures:
            print(f"  {line}")
        return 0 if not self.failures else 1


def main_for(name: str, populate) -> int:  # type: ignore[no-untyped-def]
    v = Verifier(name)
    populate(v)
    code = v.report()
    sys.exit(code)
