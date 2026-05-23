"""
Monthly strategy generator.

Produces a one-page monthly delta the founder reviews with the
strategic-bets file (`strategy/strategic_bets.md` in the private repo).
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class MonthlyStrategy:
    title: str
    body: str

    def as_markdown(self) -> str:
        return f"# {self.title}\n\n{self.body}\n"


def generate_monthly_strategy(
    *,
    month_label: str,
    bets_continue: list[str],
    bets_kill: list[str],
    bets_start: list[str],
    notes: str = "",
) -> MonthlyStrategy:
    lines: list[str] = []
    lines.append("## Continue")
    lines.extend(f"- {b}" for b in (bets_continue or ["(none)"]))
    lines.append("")
    lines.append("## Kill")
    lines.extend(f"- {b}" for b in (bets_kill or ["(none)"]))
    lines.append("")
    lines.append("## Start")
    lines.extend(f"- {b}" for b in (bets_start or ["(none)"]))
    if notes:
        lines.append("")
        lines.append("## Notes")
        lines.append(notes)
    return MonthlyStrategy(
        title=f"Monthly Strategy Review — {month_label}",
        body="\n".join(lines),
    )
