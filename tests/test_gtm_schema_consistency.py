"""Contract: committed GTM JSON schemas match their Pydantic models.

If a model changes without regenerating, this fails with the fix command.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.gen_gtm_schemas import MODELS, SCHEMA_DIR, build_schema


@pytest.mark.parametrize("slug", list(MODELS))
def test_committed_schema_matches_model(slug: str) -> None:
    model, _title = MODELS[slug]
    expected = build_schema(model, slug)
    path = SCHEMA_DIR / f"{slug}.schema.json"
    assert path.exists(), f"missing schema {path} — run: python3 scripts/gen_gtm_schemas.py"
    actual = json.loads(path.read_text(encoding="utf-8"))
    assert actual == expected, (
        f"{slug}.schema.json is out of date with its model. "
        "Run: python3 scripts/gen_gtm_schemas.py"
    )


def test_all_gtm_schemas_have_canonical_id() -> None:
    for slug in MODELS:
        schema = json.loads((SCHEMA_DIR / f"{slug}.schema.json").read_text(encoding="utf-8"))
        assert schema["$id"] == f"https://dealix.sa/schemas/{slug}.schema.json"
        assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
