from pathlib import Path
import csv
import json


def load_schema(schema_path: str) -> dict:
    return json.loads(Path(schema_path).read_text(encoding="utf-8"))


def read_headers(csv_path: str) -> list[str]:
    path = Path(csv_path)
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return reader.fieldnames or []


def read_rows(csv_path: str) -> list[dict]:
    path = Path(csv_path)
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def validate_required_headers(csv_path: str, schema_path: str) -> list[str]:
    schema = load_schema(schema_path)
    headers = read_headers(csv_path)
    failures = []
    for header in schema.get("required_headers", []):
        if header not in headers:
            failures.append(f"{csv_path} missing header: {header}")
    return failures


def validate_allowed_values(csv_path: str, schema_path: str) -> list[str]:
    schema = load_schema(schema_path)
    rows = read_rows(csv_path)
    failures = []
    field_map = {
        "allowed_stages": "stage",
        "allowed_priorities": "priority",
        "allowed_types": "type",
        "allowed_statuses": "status",
        "allowed_risk_levels": "risk_level",
        "allowed_decisions": "decision",
    }
    for allowed_key, field in field_map.items():
        if allowed_key not in schema:
            continue
        allowed = set(schema[allowed_key])
        for index, row in enumerate(rows, start=2):
            value = (row.get(field) or "").strip()
            if value not in allowed:
                failures.append(
                    f"{csv_path} row {index}: invalid {field} '{value}'"
                )
    return failures


def validate_csv_against_schema(csv_path: str, schema_path: str) -> list[str]:
    failures = []
    failures.extend(validate_required_headers(csv_path, schema_path))
    failures.extend(validate_allowed_values(csv_path, schema_path))
    return failures
