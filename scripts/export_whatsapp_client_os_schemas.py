#!/usr/bin/env python3
"""Export WhatsApp Client OS JSON Schemas from the pydantic models.

Regenerates the canonical JSON Schema files under ``dealix/contracts/schemas/``
so docs/UI/validators stay in lock-step with the code. Run from repo root:

    python3 scripts/export_whatsapp_client_os_schemas.py

CI/tests assert these files exist and match the live models.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from auto_client_acquisition.whatsapp_client_os.schemas import (
    ClientAssessment,
    ClientCard,
    InboundMessage,
    PermissionRequest,
    WhatsAppSession,
)

_OUT_DIR = _REPO_ROOT / "dealix" / "contracts" / "schemas"

# filename → pydantic model (names follow the WhatsApp Client OS plan)
_TARGETS = {
    "whatsapp_session.schema.json": WhatsAppSession,
    "whatsapp_intake.schema.json": InboundMessage,
    "whatsapp_action_card.schema.json": ClientCard,
    "client_permission.schema.json": PermissionRequest,
    "client_onboarding_assessment.schema.json": ClientAssessment,
}


def build_schema(model: type) -> dict:
    schema = model.model_json_schema()
    schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    schema["$id"] = f"https://dealix.sa/schemas/{model.__name__}.schema.json"
    return schema


def main() -> int:
    _OUT_DIR.mkdir(parents=True, exist_ok=True)
    for filename, model in _TARGETS.items():
        schema = build_schema(model)
        path = _OUT_DIR / filename
        path.write_text(json.dumps(schema, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {path.relative_to(_REPO_ROOT)}  ({model.__name__})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
