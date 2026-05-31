"""Learning Engine — processes reply signals and updates playbooks."""
from __future__ import annotations

import json
import logging
import os
from collections import defaultdict
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from auto_client_acquisition.omni_channel_os.schemas import LearningSignal, PlaybookUpdate

log = logging.getLogger(__name__)
_NO_AUTO_SEND = True

POSITIVE_SIGNALS = frozenset({"reply", "meeting_booked", "demo_requested", "proposal_requested"})
NEGATIVE_SIGNALS = frozenset({"bounce", "unsubscribe"})
NEUTRAL_SIGNALS = frozenset({"no_reply"})

_DEFAULT_SIGNALS_FILE = Path("data/learning_signals.jsonl")
_DEFAULT_PLAYBOOKS_FILE = Path("data/playbooks.json")


def _signals_path() -> Path:
    env_val = os.environ.get("DEALIX_SIGNALS_PATH", "")
    return Path(env_val) if env_val else _DEFAULT_SIGNALS_FILE


def _playbooks_path() -> Path:
    env_val = os.environ.get("DEALIX_PLAYBOOKS_PATH", "")
    return Path(env_val) if env_val else _DEFAULT_PLAYBOOKS_FILE


class LearningEngine:
    """Processes outreach signals and generates playbook updates."""

    _NO_AUTO_SEND = True

    def record_signal(self, signal: LearningSignal) -> None:
        """Persist a learning signal to the JSONL store."""
        path = _signals_path()
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("a", encoding="utf-8") as fh:
                fh.write(signal.model_dump_json() + "\n")
            log.debug(
                "learning_engine.signal_recorded signal_id=%s response=%s",
                signal.signal_id,
                signal.response_type,
            )
        except Exception as exc:
            log.warning("learning_engine.record_signal_failed error=%s", exc)

    def _load_signals(self, days: int = 7) -> list[LearningSignal]:
        """Load signals from the last N days."""
        path = _signals_path()
        if not path.exists():
            return []
        cutoff = datetime.now(UTC) - timedelta(days=days)
        signals: list[LearningSignal] = []
        try:
            for line in path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    sig = LearningSignal.model_validate_json(line)
                    # sent_at may be offset-naive; compare carefully
                    sent = sig.sent_at
                    if sent.tzinfo is None:
                        from datetime import timezone
                        sent = sent.replace(tzinfo=timezone.utc)
                    if sent >= cutoff:
                        signals.append(sig)
                except Exception:
                    pass
        except Exception as exc:
            log.warning("learning_engine.load_signals_failed error=%s", exc)
        return signals

    def analyze_signals(self, days: int = 7) -> dict[str, Any]:
        """Analyze signals from the last N days by sector, channel, and language."""
        signals = self._load_signals(days)

        by_sector: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
        by_channel: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
        by_language: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))

        for sig in signals:
            response = sig.response_type
            by_sector[sig.sector][response] += 1
            by_channel[sig.channel][response] += 1
            by_language[sig.language][response] += 1

        def _reply_rate(counts: dict[str, int]) -> float:
            total = sum(counts.values())
            if total == 0:
                return 0.0
            positive = sum(counts.get(r, 0) for r in POSITIVE_SIGNALS)
            return round(positive / total * 100, 1)

        sector_summary = {
            sec: {"counts": dict(counts), "reply_rate_pct": _reply_rate(counts)}
            for sec, counts in by_sector.items()
        }
        channel_summary = {
            ch: {"counts": dict(counts), "reply_rate_pct": _reply_rate(counts)}
            for ch, counts in by_channel.items()
        }

        return {
            "days_analyzed": days,
            "total_signals": len(signals),
            "by_sector": sector_summary,
            "by_channel": channel_summary,
            "by_language": {
                lang: dict(counts) for lang, counts in by_language.items()
            },
        }

    def generate_playbook_update(self, sector: str, channel: str) -> PlaybookUpdate:
        """Generate a PlaybookUpdate based on signal analysis for sector + channel."""
        signals = self._load_signals(days=30)
        relevant = [
            s for s in signals if s.sector == sector and s.channel == channel
        ]

        what_works: list[str] = []
        what_doesnt: list[str] = []
        best_subject_lines: list[str] = []
        best_hooks: list[str] = []
        winning_messages: list[str] = []

        positive_sigs = [s for s in relevant if s.response_type in POSITIVE_SIGNALS]
        negative_sigs = [s for s in relevant if s.response_type in NEGATIVE_SIGNALS]

        if positive_sigs:
            what_works.append(
                f"{len(positive_sigs)} positive responses recorded for {sector} via {channel}"
            )
            for sig in positive_sigs[:3]:
                if sig.response_text:
                    winning_messages.append(sig.response_text[:200])

        if negative_sigs:
            what_doesnt.append(
                f"{len(negative_sigs)} bounces/unsubscribes for {sector} via {channel}"
            )

        reply_rate = self._reply_rate(sector, channel)
        if reply_rate > 10:
            best_subject_lines.append(f"High-performing messages in {sector} (rate: {reply_rate:.1f}%)")

        return PlaybookUpdate(
            sector=sector,
            channel=channel,
            what_works=what_works,
            what_doesnt=what_doesnt,
            best_subject_lines=best_subject_lines,
            best_hooks=best_hooks,
            sample_winning_messages=winning_messages,
        )

    def get_best_subject_lines(self, sector: str, n: int = 5) -> list[str]:
        """Return the top N subject lines by reply rate for a sector."""
        signals = self._load_signals(days=30)
        positive = [
            s for s in signals
            if s.sector == sector and s.response_type in POSITIVE_SIGNALS
        ]
        subjects: dict[str, int] = defaultdict(int)
        for sig in positive:
            if sig.response_text:
                subjects[sig.response_text[:100]] += 1
        sorted_subjects = sorted(subjects.items(), key=lambda x: -x[1])
        return [s for s, _ in sorted_subjects[:n]]

    def get_best_hooks(self, sector: str, channel: str, n: int = 5) -> list[str]:
        """Return the top N opening hooks by engagement for sector + channel."""
        signals = self._load_signals(days=30)
        positive = [
            s for s in signals
            if s.sector == sector
            and s.channel == channel
            and s.response_type in POSITIVE_SIGNALS
        ]
        hooks: dict[str, int] = defaultdict(int)
        for sig in positive:
            if sig.offer:
                hooks[sig.offer] += 1
        sorted_hooks = sorted(hooks.items(), key=lambda x: -x[1])
        return [h for h, _ in sorted_hooks[:n]]

    def daily_learning_report(self) -> dict[str, Any]:
        """Generate a daily learning summary for founder review."""
        analysis = self.analyze_signals(days=1)
        weekly = self.analyze_signals(days=7)

        top_channels = sorted(
            weekly["by_channel"].items(),
            key=lambda x: x[1].get("reply_rate_pct", 0),
            reverse=True,
        )

        return {
            "date": datetime.now(UTC).strftime("%Y-%m-%d"),
            "today_signal_count": analysis["total_signals"],
            "week_signal_count": weekly["total_signals"],
            "top_channels_by_reply_rate": [
                {"channel": ch, "reply_rate_pct": data.get("reply_rate_pct", 0)}
                for ch, data in top_channels[:5]
            ],
            "by_sector_weekly": weekly["by_sector"],
            "insight": (
                "No signals recorded yet — keep sending and track replies."
                if weekly["total_signals"] == 0
                else f"{weekly['total_signals']} signals in last 7 days."
            ),
        }

    def _reply_rate(self, sector: str, channel: str) -> float:
        """Calculate reply rate for the sector + channel combination (last 30 days)."""
        signals = self._load_signals(days=30)
        relevant = [
            s for s in signals if s.sector == sector and s.channel == channel
        ]
        if not relevant:
            return 0.0
        positive = sum(1 for s in relevant if s.response_type in POSITIVE_SIGNALS)
        return round(positive / len(relevant) * 100, 1)


__all__ = [
    "NEGATIVE_SIGNALS",
    "NEUTRAL_SIGNALS",
    "POSITIVE_SIGNALS",
    "LearningEngine",
]
