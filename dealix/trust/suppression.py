"""
Suppression list — enforces `docs/trust/SUPPRESSION_LIST_POLICY.md`.

Every external send path must call `is_suppressed(identifier)` (or use
`assert_not_suppressed`) before reaching an external API. The list is
monotonic (additions only) — removals require founder + advisor signoff
and a logged decision.

This module is a pure in-memory implementation backed by a CSV file. It
intentionally keeps a small surface area so it's auditable.
"""

from __future__ import annotations

import csv
import re
import threading
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path


class SuppressionViolation(Exception):  # noqa: N818 — incident vocabulary
    """Raised when a send is attempted to a suppression-list contact."""

    def __init__(self, identifier: str, reason: str = "") -> None:
        super().__init__(
            f"Suppression violation: {identifier} is on the suppression list."
            + (f" Reason: {reason}" if reason else "")
        )
        self.identifier = identifier
        self.reason = reason


@dataclass(frozen=True)
class SuppressionEntry:
    identifier_type: str  # email | linkedin | phone | domain
    identifier_value: str
    added_at: datetime
    reason: str
    source: str
    owner: str


_LOCK = threading.Lock()
_LINKEDIN_SLUG = re.compile(r"linkedin\.com/in/([^/?#]+)", re.IGNORECASE)
_PHONE_DIGITS = re.compile(r"\D")


def _normalize_email(value: str) -> str:
    v = value.strip().lower()
    if "@" not in v:
        return v
    local, _, domain = v.partition("@")
    local = local.split("+", 1)[0]
    return f"{local}@{domain}"


def _normalize_linkedin(value: str) -> str:
    v = value.strip().lower()
    m = _LINKEDIN_SLUG.search(v)
    if m:
        return f"linkedin:{m.group(1).rstrip('/')}"
    return f"linkedin:{v.rstrip('/')}"


def _normalize_phone(value: str) -> str:
    digits = _PHONE_DIGITS.sub("", value)
    return f"phone:{digits}"


def _normalize_domain(value: str) -> str:
    v = value.strip().lower()
    v = re.sub(r"^https?://", "", v)
    v = v.split("/", 1)[0]
    return f"domain:{v}"


def normalize(identifier_type: str, identifier_value: str) -> str:
    """Normalize an identifier into a canonical comparable form."""
    t = identifier_type.lower().strip()
    if t == "email":
        return _normalize_email(identifier_value)
    if t == "linkedin":
        return _normalize_linkedin(identifier_value)
    if t == "phone":
        return _normalize_phone(identifier_value)
    if t == "domain":
        return _normalize_domain(identifier_value)
    return identifier_value.strip().lower()


class SuppressionList:
    """In-memory suppression set with CSV backing.

    The CSV path lives in the private repo (`trust/suppression_list.csv`).
    The class only reads; additions go through `add()` which also appends
    to the CSV. Removals are not implemented at the module level by design.
    """

    def __init__(self, csv_path: Path | None = None) -> None:
        self._csv_path = csv_path
        self._entries: dict[str, SuppressionEntry] = {}
        if csv_path and csv_path.exists():
            self._load_from_csv()

    def _load_from_csv(self) -> None:
        with self._csv_path.open(encoding="utf-8") as f:  # type: ignore[union-attr]
            reader = csv.DictReader(f)
            for row in reader:
                key = normalize(row["identifier_type"], row["identifier_value"])
                self._entries[key] = SuppressionEntry(
                    identifier_type=row["identifier_type"],
                    identifier_value=row["identifier_value"],
                    added_at=datetime.fromisoformat(row["added_at"]),
                    reason=row.get("reason", ""),
                    source=row.get("source", ""),
                    owner=row.get("owner", ""),
                )

    def add(
        self,
        identifier_type: str,
        identifier_value: str,
        reason: str,
        source: str,
        owner: str,
    ) -> SuppressionEntry:
        """Add a contact to suppression. Monotonic: never removes."""
        key = normalize(identifier_type, identifier_value)
        with _LOCK:
            if key in self._entries:
                return self._entries[key]
            entry = SuppressionEntry(
                identifier_type=identifier_type,
                identifier_value=identifier_value,
                added_at=datetime.now(UTC),
                reason=reason,
                source=source,
                owner=owner,
            )
            self._entries[key] = entry
            if self._csv_path:
                self._append_to_csv(entry)
            return entry

    def _append_to_csv(self, entry: SuppressionEntry) -> None:
        path = self._csv_path
        assert path is not None
        write_header = not path.exists()
        with path.open("a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            if write_header:
                writer.writerow(
                    ["identifier_type", "identifier_value", "added_at", "reason", "source", "owner"]
                )
            writer.writerow(
                [
                    entry.identifier_type,
                    entry.identifier_value,
                    entry.added_at.isoformat(),
                    entry.reason,
                    entry.source,
                    entry.owner,
                ]
            )

    def is_suppressed(self, identifier_type: str, identifier_value: str) -> bool:
        key = normalize(identifier_type, identifier_value)
        return key in self._entries

    def get(self, identifier_type: str, identifier_value: str) -> SuppressionEntry | None:
        key = normalize(identifier_type, identifier_value)
        return self._entries.get(key)

    def __len__(self) -> int:
        return len(self._entries)

    def __iter__(self) -> Iterable[SuppressionEntry]:
        return iter(self._entries.values())


# Module-level default list (in-memory). Production code should construct
# a SuppressionList with the real CSV path from the private repo.
_default_list = SuppressionList()


def is_suppressed(identifier_type: str, identifier_value: str) -> bool:
    """Check the default suppression list."""
    return _default_list.is_suppressed(identifier_type, identifier_value)


def assert_not_suppressed(identifier_type: str, identifier_value: str) -> None:
    """Raise SuppressionViolation if the contact is on the suppression list."""
    entry = _default_list.get(identifier_type, identifier_value)
    if entry is not None:
        raise SuppressionViolation(entry.identifier_value, entry.reason)


def default_list() -> SuppressionList:
    return _default_list


def set_default_list(suppression_list: SuppressionList) -> None:
    """Replace the module-level default. Used for production bootstrap and tests."""
    global _default_list
    _default_list = suppression_list


__all__ = [
    "SuppressionEntry",
    "SuppressionList",
    "SuppressionViolation",
    "assert_not_suppressed",
    "default_list",
    "is_suppressed",
    "normalize",
    "set_default_list",
]
