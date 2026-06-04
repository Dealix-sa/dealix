"""Shared helpers for the verification scripts."""

from __future__ import annotations

from dataclasses import dataclass, asdict


@dataclass
class Check:
    name: str
    passed: bool
    critical: bool = True
    detail: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def summarize(checks: list[Check]) -> dict:
    critical = [c for c in checks if c.critical]
    critical_failed = [c for c in critical if not c.passed]
    warnings = [c for c in checks if not c.critical and not c.passed]
    return {
        "total": len(checks),
        "passed": sum(1 for c in checks if c.passed),
        "failed": sum(1 for c in checks if not c.passed),
        "critical_failed": len(critical_failed),
        "warnings": len(warnings),
        "pass": len(critical_failed) == 0,
        "checks": [c.to_dict() for c in checks],
    }


def print_checks(prefix: str, checks: list[Check]) -> None:
    for c in checks:
        status = "PASS" if c.passed else ("WARN" if not c.critical else "FAIL")
        line = f"[{prefix}]   {status}  {c.name}"
        if c.detail:
            line += f" — {c.detail}"
        print(line)
