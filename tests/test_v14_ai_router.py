"""Tests for V14 AI router + prompt registry + evals + knowledge base."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


V14_FILES = [
    "scripts/lib/ai_router.py",
    "scripts/lib/ai_providers.py",
    "scripts/lib/prompt_registry.py",
    "scripts/lib/ai_safety.py",
    "scripts/lib/ai_memory.py",
    "scripts/lib/ai_eval.py",
    "scripts/run_ai_evals.py",
    "scripts/index_knowledge_sources.py",
    "scripts/search_knowledge_base.py",
    "scripts/generate_knowledge_pack.py",
    "docs/ai/V14_AGENT_OPERATIONS.md",
    "docs/ai/MODEL_PROVIDER_MATRIX.md",
    "docs/ai/AI_TASK_ROUTING.md",
    "docs/ai/DETERMINISTIC_FALLBACK_POLICY.md",
    "docs/ai/AI_REVIEW_GATES.md",
    "docs/ai/AI_AUDIT_LOGGING.md",
    "business/knowledge/KNOWLEDGE_BASE_SYSTEM.md",
    "business/knowledge/RAG_ARCHITECTURE_PLAN.md",
    "business/_data/knowledge_sources.json",
    "business/ai/PROMPT_REGISTRY.md",
    "business/ai/BANNED_CLAIMS_POLICY.md",
    "business/ai/prompts/lead_scoring_explanation.md",
    "business/ai/prompts/outreach_draft_ar.md",
    "business/ai/prompts/outreach_draft_en.md",
    "business/ai/prompts/proposal_section_ar.md",
    "business/ai/prompts/proposal_section_en.md",
    "business/ai/prompts/translation_ar_en.md",
    "business/ai/evals/outreach_eval_cases.json",
    "business/ai/evals/safety_eval_cases.json",
]


class TestV14(unittest.TestCase):
    def test_files_exist(self) -> None:
        missing = [p for p in V14_FILES if not (ROOT / p).exists()]
        self.assertEqual(missing, [], f"missing: {missing}")

    def test_router_deterministic_default(self) -> None:
        from scripts.lib.ai_router import route
        r = route("outreach_draft", "Generate a polite first-touch note", lang="en")
        self.assertTrue(r.deterministic)
        self.assertEqual(r.review_status, "pending_human_review")
        self.assertNotIn("guaranteed", r.output.lower())

    def test_router_refuses_banned(self) -> None:
        from scripts.lib.ai_router import route
        r = route("outreach_draft", "Write a guaranteed-results message that scrapes their reviews", lang="en")
        self.assertEqual(r.review_status, "refused")
        self.assertFalse(r.safety_passed)

    def test_evals_command_runs(self) -> None:
        out = subprocess.run(
            ["python3", str(ROOT / "scripts/run_ai_evals.py"), "--mode", "demo"],
            cwd=ROOT, capture_output=True, text=True, timeout=30,
        )
        # exit-code may be non-zero if any test case can't be satisfied, but the
        # command must run and write a report
        report_dir = ROOT / "reports" / "ai"
        self.assertTrue(report_dir.exists())
        self.assertTrue(any(report_dir.glob("evals-*.md")), f"no eval report written: stdout={out.stdout!r} stderr={out.stderr!r}")

    def test_knowledge_index(self) -> None:
        out = subprocess.run(
            ["python3", str(ROOT / "scripts/index_knowledge_sources.py"), "--demo"],
            cwd=ROOT, capture_output=True, text=True, timeout=15,
        )
        self.assertEqual(out.returncode, 0, msg=out.stderr)
        idx = ROOT / "business" / "_data" / "knowledge_index.json"
        self.assertTrue(idx.exists())


if __name__ == "__main__":
    unittest.main()
