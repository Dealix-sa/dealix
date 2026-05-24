"""
Conversation memory — rolling window + auto-summary.
ذاكرة المحادثة — نافذة متحركة مع تلخيص تلقائي.

Stores user/assistant turns, prunes by max-turns + max-chars, and produces
a compact "running summary" prefix usable as a system message for the LLM
gateway. No external state — caller persists if needed.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Iterable, Literal

from dealix.intelligence.layers.summarizer import ExtractiveSummarizer

Role = Literal["system", "user", "assistant", "tool"]


@dataclass(frozen=True)
class Turn:
    role: Role
    content: str
    timestamp: float = field(default_factory=time.time)
    metadata: dict = field(default_factory=dict)


@dataclass
class MemorySnapshot:
    running_summary: str
    recent_turns: tuple[Turn, ...]
    total_turns: int
    total_chars: int
    pruned_turns: int


class ConversationMemory:
    """Rolling memory with auto-summarization when over budget."""

    def __init__(
        self,
        *,
        max_turns: int = 20,
        max_chars: int = 8000,
        summarizer: ExtractiveSummarizer | None = None,
        summary_top_k: int = 3,
    ) -> None:
        if max_turns < 2:
            raise ValueError("max_turns must be >= 2")
        if max_chars < 200:
            raise ValueError("max_chars must be >= 200")
        self.max_turns = max_turns
        self.max_chars = max_chars
        self._summarizer = summarizer or ExtractiveSummarizer(top_k=summary_top_k)
        self._summary_top_k = summary_top_k
        self._turns: list[Turn] = []
        self._running_summary: str = ""
        self._pruned_turns = 0

    # ── Public ─────────────────────────────────────────────────────
    def add(self, role: Role, content: str, *, metadata: dict | None = None) -> Turn:
        turn = Turn(role=role, content=content, metadata=dict(metadata or {}))
        self._turns.append(turn)
        self._prune_if_needed()
        return turn

    def add_many(self, turns: Iterable[tuple[Role, str]]) -> int:
        count = 0
        for role, content in turns:
            self.add(role, content)
            count += 1
        return count

    def snapshot(self) -> MemorySnapshot:
        total_chars = sum(len(t.content) for t in self._turns)
        return MemorySnapshot(
            running_summary=self._running_summary,
            recent_turns=tuple(self._turns),
            total_turns=len(self._turns),
            total_chars=total_chars,
            pruned_turns=self._pruned_turns,
        )

    def reset(self) -> None:
        self._turns.clear()
        self._running_summary = ""
        self._pruned_turns = 0

    def for_llm(self, *, system_prompt: str | None = None) -> list[dict[str, str]]:
        msgs: list[dict[str, str]] = []
        if system_prompt:
            msgs.append({"role": "system", "content": system_prompt})
        if self._running_summary:
            msgs.append(
                {
                    "role": "system",
                    "content": f"Conversation summary so far:\n{self._running_summary}",
                }
            )
        for t in self._turns:
            if t.role == "tool":
                continue
            msgs.append({"role": t.role, "content": t.content})
        return msgs

    # ── Internals ─────────────────────────────────────────────────
    def _prune_if_needed(self) -> None:
        if len(self._turns) <= self.max_turns and self._char_budget_ok():
            return
        # Drop oldest half + summarize them into running_summary.
        drop_count = max(1, len(self._turns) // 2)
        dropping = self._turns[:drop_count]
        self._turns = self._turns[drop_count:]
        self._pruned_turns += drop_count
        joined = "\n".join(
            f"{t.role}: {t.content}" for t in dropping if t.role in ("user", "assistant")
        )
        if not joined.strip():
            return
        new_summary = self._summarizer.summarize(
            joined, top_k=self._summary_top_k
        ).summary
        if self._running_summary:
            self._running_summary = (self._running_summary + " " + new_summary).strip()
        else:
            self._running_summary = new_summary
        # Trim running summary to avoid unbounded growth.
        if len(self._running_summary) > self.max_chars // 2:
            re_summary = self._summarizer.summarize(
                self._running_summary, top_k=self._summary_top_k
            ).summary
            self._running_summary = re_summary or self._running_summary[: self.max_chars // 2]

    def _char_budget_ok(self) -> bool:
        total = sum(len(t.content) for t in self._turns)
        return total <= self.max_chars
