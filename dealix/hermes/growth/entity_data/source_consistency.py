from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SourceConsistencyReport:
    consistent: bool
    differences: list[str]


def check_source_consistency(
    canonical: dict[str, object], external_sources: dict[str, dict[str, object]]
) -> SourceConsistencyReport:
    differences: list[str] = []
    for source_name, source_data in external_sources.items():
        for field, canonical_value in canonical.items():
            if field not in source_data:
                continue
            if source_data[field] != canonical_value:
                differences.append(
                    f"{source_name}.{field}: {source_data[field]!r} "
                    f"!= canonical {canonical_value!r}"
                )
    return SourceConsistencyReport(
        consistent=not differences, differences=differences
    )
