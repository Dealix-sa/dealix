"""Five-level data classification — the foundation of every policy check."""

from __future__ import annotations

from enum import StrEnum


class DataClass(StrEnum):
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    CONFIDENTIAL = "CONFIDENTIAL"
    RESTRICTED = "RESTRICTED"
    SOVEREIGN = "SOVEREIGN"


# Heuristic field-name classifier — production swaps in a data catalog.
_PATTERNS: dict[str, DataClass] = {
    "password": DataClass.RESTRICTED,
    "secret": DataClass.RESTRICTED,
    "token": DataClass.RESTRICTED,
    "private_key": DataClass.SOVEREIGN,
    "iban": DataClass.RESTRICTED,
    "national_id": DataClass.RESTRICTED,
    "id_number": DataClass.RESTRICTED,
    "email": DataClass.CONFIDENTIAL,
    "phone": DataClass.CONFIDENTIAL,
    "salary": DataClass.RESTRICTED,
    "cap_table": DataClass.SOVEREIGN,
    "pricing": DataClass.CONFIDENTIAL,
}


def classify_field(field_name: str) -> DataClass:
    lowered = field_name.lower()
    for needle, cls in _PATTERNS.items():
        if needle in lowered:
            return cls
    return DataClass.INTERNAL


def is_pii(cls: DataClass) -> bool:
    return cls in {DataClass.CONFIDENTIAL, DataClass.RESTRICTED}
