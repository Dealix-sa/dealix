#!/usr/bin/env python3
"""Generate canonical JSON Schemas for the Market Production OS data objects.

Schemas are derived from the Pydantic models so they cannot drift. Run after
changing any GTM record model:

    python3 scripts/gen_gtm_schemas.py

A companion test (``tests/test_gtm_schema_consistency.py``) fails if a committed
schema no longer matches its model — keeping the contract honest.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pydantic import BaseModel

from auto_client_acquisition.gtm_os.outreach_draft import OutreachDraft
from auto_client_acquisition.gtm_os.records import (
    CompanySignal,
    Prospect,
    Reply,
    SuppressionEntry,
)
from auto_client_acquisition.gtm_os.sending_ramp import SendingPlan

SCHEMA_DIR = Path(__file__).resolve().parents[1] / "dealix" / "contracts" / "schemas"

# slug -> (model, human title)
MODELS: dict[str, tuple[type[BaseModel], str]] = {
    "outreach_draft": (OutreachDraft, "OutreachDraft"),
    "sending_plan": (SendingPlan, "SendingPlan"),
    "prospect": (Prospect, "Prospect"),
    "company_signal": (CompanySignal, "CompanySignal"),
    "reply": (Reply, "Reply"),
    "suppression_entry": (SuppressionEntry, "SuppressionEntry"),
}


def build_schema(model: type[BaseModel], slug: str) -> dict[str, Any]:
    """Model JSON schema + the repo's canonical ``$schema`` / ``$id`` envelope."""
    schema = model.model_json_schema()
    schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    schema["$id"] = f"https://dealix.sa/schemas/{slug}.schema.json"
    return schema


def main() -> int:
    SCHEMA_DIR.mkdir(parents=True, exist_ok=True)
    for slug, (model, _title) in MODELS.items():
        schema = build_schema(model, slug)
        out = SCHEMA_DIR / f"{slug}.schema.json"
        out.write_text(json.dumps(schema, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"wrote {out.relative_to(SCHEMA_DIR.parents[2])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
