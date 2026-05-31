"""
DataClassification — labels for fields and records so the platform can
make automated isolation / redaction / retention decisions.
"""

from __future__ import annotations

from enum import StrEnum


class DataClassification(StrEnum):
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    CONFIDENTIAL = "CONFIDENTIAL"
    REGULATED = "REGULATED"  # personal data, PDPL scope
    SOVEREIGN = "SOVEREIGN"  # Sami-only, never leaves the platform


_FIELD_HEURISTICS = {
    DataClassification.SOVEREIGN: ("sovereign_memory", "internal_strategy", "founder_notes"),
    DataClassification.REGULATED: ("phone", "email", "id_number", "iban", "pan"),
    DataClassification.CONFIDENTIAL: ("contract", "price", "margin", "customer_data", "deal"),
    DataClassification.INTERNAL: ("workflow", "playbook", "policy", "agent"),
}


def classify_field(field_name: str) -> DataClassification:
    f = field_name.lower()
    for cls, markers in _FIELD_HEURISTICS.items():
        for marker in markers:
            if marker in f:
                return cls
    return DataClassification.PUBLIC
