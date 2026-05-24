"""Shared helpers for Dealix verifier scripts."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class VerifyResult:
    name: str
    passed: bool
    notes: list[str] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "passed": self.passed,
            "notes": list(self.notes),
            "missing": list(self.missing),
        }


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def must_exist(rel_paths: list[str], result: VerifyResult) -> None:
    root = repo_root()
    for rel in rel_paths:
        if not (root / rel).exists():
            result.missing.append(rel)
    if result.missing:
        result.passed = False
        result.notes.append(f"{len(result.missing)} missing path(s)")


def print_and_exit(result: VerifyResult) -> int:
    status = "PASS" if result.passed else "FAIL"
    print(f"{result.name}: {status}")
    for note in result.notes:
        print(f"  · {note}")
    for path in result.missing:
        print(f"  · missing: {path}")
    return 0 if result.passed else 1
