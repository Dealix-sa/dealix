from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "verify_tool_radar.py"
REGISTRY = ROOT / "dealix_july_2026_tool_radar.json"
if not SCRIPT.exists():
    SCRIPT = ROOT / "scripts" / "agents" / "verify_tool_intake.py"
    REGISTRY = ROOT / "dealix" / "registers" / "tool_intake_july_2026.json"

SPEC = importlib.util.spec_from_file_location("verify_tool_radar", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ToolRadarValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = json.loads(
            REGISTRY.read_text(encoding="utf-8")
        )

    def test_current_registry_is_valid(self) -> None:
        self.assertEqual(MODULE.validate(self.payload), [])

    def test_duplicate_id_is_rejected(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["items"].append(copy.deepcopy(payload["items"][0]))
        errors = MODULE.validate(payload)
        self.assertTrue(any("duplicate ids" in error for error in errors))

    def test_out_of_window_release_is_rejected(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["items"][0]["release_date"] = "2026-06-30"
        errors = MODULE.validate(payload)
        self.assertTrue(any("outside the research window" in error for error in errors))

    def test_unverified_license_must_be_held(self) -> None:
        payload = copy.deepcopy(self.payload)
        item = payload["items"][-2]
        self.assertEqual(item["license"], "unverified")
        item["decision"] = "pilot"
        errors = MODULE.validate(payload)
        self.assertTrue(any("unverified license must be held" in error for error in errors))

    def test_summary_counts_all_items(self) -> None:
        result = MODULE.summary(self.payload)
        self.assertEqual(result["items"], len(self.payload["items"]))
        self.assertEqual(sum(result["by_decision"].values()), result["items"])


if __name__ == "__main__":
    unittest.main()
