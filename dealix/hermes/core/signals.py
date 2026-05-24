"""
In-memory Signal store for the Hermes Kernel.

Replaceable with a persistent backend later. The store is intentionally
narrow: append-only writes, read-by-id, list-all.
"""

from __future__ import annotations

from uuid import uuid4

from dealix.hermes.core.schemas import HermesSignal


class SignalStore:
    def __init__(self) -> None:
        self._signals: dict[str, HermesSignal] = {}

    def add(self, signal: HermesSignal) -> str:
        signal_id = str(uuid4())
        self._signals[signal_id] = signal
        return signal_id

    def get(self, signal_id: str) -> HermesSignal | None:
        return self._signals.get(signal_id)

    def list_all(self) -> list[tuple[str, HermesSignal]]:
        return list(self._signals.items())

    def count(self) -> int:
        return len(self._signals)


_default_store = SignalStore()


def default_store() -> SignalStore:
    return _default_store
