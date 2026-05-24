"""Venture Portfolio — single view across active verticals."""

from __future__ import annotations

from threading import RLock

from dealix.hermes.ventures.vertical_launcher import VerticalTest


class VenturePortfolio:
    def __init__(self) -> None:
        self._items: dict[str, VerticalTest] = {}
        self._lock = RLock()

    def add(self, test: VerticalTest) -> None:
        with self._lock:
            self._items[test.vertical] = test

    def list(self) -> list[VerticalTest]:
        with self._lock:
            return list(self._items.values())

    def clear(self) -> None:
        with self._lock:
            self._items.clear()
