#!/usr/bin/env python3
"""Validate the canonical Company Intelligence entity ownership registry."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

REGISTRY = Path(__file__).resolve().parents[1] / "dealix/registers/company_intelligence_entity_ownership.json"
REQUIRED_ENTITY_KEYS = {
    "name",
    "owner",
    "canonical_boundary",
    "status",
    "external_source_of_truth_allowed",
    "required_fields",
    "forbidden_parallel_names",
}
REQUIRED_CANONICAL_ENTITIES = {
    "Tenant", "CompanyBrain", "Offer", "Persona", "Company", "Contact",
    "Source", "ConsentBasis", "Signal", "Relationship", "Opportunity",
    "PartnershipOpportunity", "DepartmentPlan", "Action", "Draft", "Approval",
    "Proposal", "OutcomeEvent", "ProofEvent", "LearningEvent", "PlaybookVersion",
    "DailyCommand",
}


def load_registry(path: Path = REGISTRY) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_registry(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    entities = data.get("entities")
    if not isinstance(entities, list) or not entities:
        return ["entities must be a non-empty list"]

    names: set[str] = set()
    aliases: set[str] = set()
    for index, entity in enumerate(entities):
        if not isinstance(entity, dict):
            errors.append(f"entities[{index}] must be an object")
            continue
        missing = REQUIRED_ENTITY_KEYS - entity.keys()
        if missing:
            errors.append(f"{entity.get('name', index)} missing keys: {sorted(missing)}")
            continue
        name = entity["name"]
        if name in names:
            errors.append(f"duplicate canonical entity: {name}")
        names.add(name)
        if entity["external_source_of_truth_allowed"] is not False:
            errors.append(f"{name} must remain Dealix-owned")
        if not entity["required_fields"]:
            errors.append(f"{name} must define required_fields")
        for alias in entity["forbidden_parallel_names"]:
            if alias in aliases or alias in names:
                errors.append(f"duplicate or colliding alias: {alias}")
            aliases.add(alias)

    missing_entities = REQUIRED_CANONICAL_ENTITIES - names
    if missing_entities:
        errors.append(f"missing canonical entities: {sorted(missing_entities)}")
    collisions = names & aliases
    if collisions:
        errors.append(f"canonical names collide with aliases: {sorted(collisions)}")
    return errors


def main() -> int:
    try:
        data = load_registry()
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL company_intelligence_entity_ownership: {exc}")
        return 1
    errors = validate_registry(data)
    if errors:
        print("FAIL company_intelligence_entity_ownership")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"PASS company_intelligence_entity_ownership {len(data['entities'])} entities")
    return 0


if __name__ == "__main__":
    sys.exit(main())
