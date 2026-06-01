#!/usr/bin/env python3
"""
validate_os_schemas.py
======================
Validates JSON schemas in os/schemas/ using jsonschema library.
Also validates example files against their schemas if examples/ exists.
Exits 0 on success, 1 on any error.

Usage:
    python scripts/validate_os_schemas.py
"""

import sys
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OS_DIR = REPO_ROOT / "os"
SCHEMAS_DIR = OS_DIR / "schemas"
EXAMPLES_DIR = OS_DIR / "examples"

# Map example files to their schema
EXAMPLE_SCHEMA_MAP = {
    "company_fm_ksa.json": "company",
    "company_legal_ksa.json": "company",
    "company_international_uae.json": "company",
    "persuasion_dossier_legal.json": "persuasion-dossier",
    "opportunity_audit.json": "opportunity",
    "project_pilot.json": "project",
}

try:
    import jsonschema
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def validate_schema_meta(schema: dict, schema_path: Path) -> list[str]:
    """Check that a schema has required meta-fields."""
    errors = []
    required_meta = ["$schema", "title", "type", "properties"]
    for field in required_meta:
        if field not in schema:
            errors.append(f"Missing meta-field '{field}' in {schema_path.name}")
    if schema.get("type") != "object":
        errors.append(f"Schema type must be 'object': {schema_path.name}")
    return errors


def validate_example_against_schema(example_path: Path, schema: dict) -> list[str]:
    """Validate an example file against a schema. Requires jsonschema."""
    if not JSONSCHEMA_AVAILABLE:
        return []  # Skip if not available

    try:
        data = load_json(example_path)
        jsonschema.validate(instance=data, schema=schema)
        return []
    except jsonschema.ValidationError as e:
        return [f"Schema validation failed for {example_path.name}: {e.message}"]
    except jsonschema.SchemaError as e:
        return [f"Invalid schema for validation: {e.message}"]
    except Exception as e:
        return [f"Error validating {example_path.name}: {e}"]


def main() -> int:
    errors = []
    ok_count = 0

    print("=" * 60)
    print("Dealix OS Schema Validation")
    print("=" * 60)

    if not JSONSCHEMA_AVAILABLE:
        print("\nWARNING: 'jsonschema' package not installed.")
        print("Install with: pip install jsonschema")
        print("Skipping JSON schema validation against examples.")
        print("Running meta-structure checks only.\n")

    # 1. Find and validate all schema files
    print("\n[Schema Meta-Validation]")
    schema_files = list(SCHEMAS_DIR.glob("*.schema.json")) if SCHEMAS_DIR.exists() else []

    if not schema_files:
        print("  [WARN] No schema files found in os/schemas/")
        errors.append("os/schemas/ is empty or missing")
    else:
        for schema_path in sorted(schema_files):
            try:
                schema = load_json(schema_path)
                meta_errors = validate_schema_meta(schema, schema_path)
                if meta_errors:
                    for e in meta_errors:
                        print(f"  [FAIL] {e}")
                        errors.append(e)
                else:
                    print(f"  [OK]   {schema_path.name}")
                    ok_count += 1
            except json.JSONDecodeError as e:
                err = f"JSON parse error in {schema_path.name}: {e}"
                print(f"  [FAIL] {err}")
                errors.append(err)

    # 2. Validate example files against schemas
    if EXAMPLES_DIR.exists() and JSONSCHEMA_AVAILABLE:
        print("\n[Example Validation Against Schemas]")
        for example_name, schema_name in EXAMPLE_SCHEMA_MAP.items():
            example_path = EXAMPLES_DIR / example_name
            schema_path = SCHEMAS_DIR / f"{schema_name}.schema.json"

            if not example_path.exists():
                print(f"  [SKIP] {example_name} (not yet created)")
                continue
            if not schema_path.exists():
                print(f"  [WARN] Schema missing for {example_name}: {schema_name}.schema.json")
                continue

            schema = load_json(schema_path)
            example_errors = validate_example_against_schema(example_path, schema)
            if example_errors:
                for e in example_errors:
                    print(f"  [FAIL] {e}")
                    errors.append(e)
            else:
                print(f"  [OK]   {example_name} validates against {schema_name}.schema.json")
                ok_count += 1

    # 3. Required schemas must exist
    print("\n[Required Schema Existence]")
    required = [
        "company", "contact", "opportunity", "project",
        "persuasion-dossier", "draft-queue", "channel-job",
        "execution-log", "reply", "finance",
    ]
    for name in required:
        path = SCHEMAS_DIR / f"{name}.schema.json"
        if path.exists():
            print(f"  [OK]   {name}.schema.json exists")
        else:
            err = f"Missing required schema: {name}.schema.json"
            print(f"  [FAIL] {err}")
            errors.append(err)

    # Summary
    print("\n" + "=" * 60)
    print(f"Results: {ok_count} OK, {len(errors)} error(s)")

    if errors:
        print("\nErrors:")
        for e in errors:
            print(f"  - {e}")
        print("\nFix all errors before proceeding.")
        return 1

    print("\nAll schema validations passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
