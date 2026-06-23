"""Guard the founder ledgers (ledgers/*.json) against their schemas/contract.

Pure stdlib so it stays fast and always-collectable inside the repo's existing
``pytest --cov`` gate — adding the Founder-OS ledgers without touching any
workflow YAML. If a ledger drifts (bad enum, missing field, duplicate id,
broken JSON), CI goes red here.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.check_ledgers import CONTRACT, validate_all

LEDGERS_DIR = ROOT / "ledgers"


def test_validator_passes_on_committed_ledgers() -> None:
    errors = validate_all(ROOT)
    assert errors == [], "Ledger contract violations:\n" + "\n".join(errors)


def test_every_ledger_has_a_schema_and_data_file() -> None:
    for name in CONTRACT:
        assert (LEDGERS_DIR / f"{name}.json").exists(), f"missing ledgers/{name}.json"
        assert (LEDGERS_DIR / f"{name}.schema.json").exists(), f"missing ledgers/{name}.schema.json"


def test_schema_files_are_valid_json_schema_objects() -> None:
    for name in CONTRACT:
        schema = json.loads((LEDGERS_DIR / f"{name}.schema.json").read_text(encoding="utf-8"))
        assert schema.get("$schema", "").startswith("https://json-schema.org/")
        assert "$defs" in schema, f"{name}.schema.json must declare a $defs block"
        assert schema["properties"]["ledger"]["const"] == name


def test_data_files_declare_matching_ledger_name() -> None:
    for name in CONTRACT:
        data = json.loads((LEDGERS_DIR / f"{name}.json").read_text(encoding="utf-8"))
        assert data["ledger"] == name
        assert isinstance(data["records"], list)
