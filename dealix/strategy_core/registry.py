"""Strict YAML strategy loading with duplicate and source checks."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from .models import StrategyDefinition


class StrategyRegistryError(RuntimeError):
    pass


@dataclass(frozen=True)
class RegisteredStrategy:
    definition: StrategyDefinition
    source_path: Path


class StrategyRegistry:
    def __init__(self, entries: tuple[RegisteredStrategy, ...]) -> None:
        self._entries = entries
        self._by_id = {entry.definition.strategy_id: entry for entry in entries}

    @classmethod
    def from_directory(cls, directory: Path, *, require_nonempty: bool = True) -> "StrategyRegistry":
        if not directory.is_dir():
            raise StrategyRegistryError(f"strategy directory does not exist: {directory}")
        paths = sorted([*directory.glob("*.yaml"), *directory.glob("*.yml")])
        if require_nonempty and not paths:
            raise StrategyRegistryError(f"strategy directory contains no YAML files: {directory}")
        entries: list[RegisteredStrategy] = []
        seen: dict[str, Path] = {}
        for path in paths:
            try:
                payload = yaml.safe_load(path.read_text(encoding="utf-8"))
            except (OSError, yaml.YAMLError) as exc:
                raise StrategyRegistryError(f"cannot load strategy YAML: {path}") from exc
            if not isinstance(payload, dict):
                raise StrategyRegistryError(f"{path.name}: top-level YAML must be an object")
            try:
                definition = StrategyDefinition.from_dict(payload)
            except (TypeError, ValueError) as exc:
                raise StrategyRegistryError(f"{path.name}: invalid strategy: {exc}") from exc
            previous = seen.get(definition.strategy_id)
            if previous is not None:
                raise StrategyRegistryError(
                    f"duplicate strategy id {definition.strategy_id!r}: {previous.name}, {path.name}"
                )
            seen[definition.strategy_id] = path
            entries.append(RegisteredStrategy(definition=definition, source_path=path))
        return cls(tuple(entries))

    def all(self) -> tuple[RegisteredStrategy, ...]:
        return self._entries

    def active(self) -> tuple[RegisteredStrategy, ...]:
        return tuple(
            sorted(
                (entry for entry in self._entries if entry.definition.enabled),
                key=lambda entry: (-entry.definition.priority, entry.definition.strategy_id),
            )
        )

    def get(self, strategy_id: str) -> RegisteredStrategy | None:
        return self._by_id.get(strategy_id.strip().casefold())

    def __len__(self) -> int:
        return len(self._entries)
