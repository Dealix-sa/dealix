"""Tests for V11 CRM admin UI + API routes."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

V11_PAGES = [
    "apps/web/app/crm/page.tsx",
    "apps/web/app/crm/accounts/page.tsx",
    "apps/web/app/crm/accounts/[id]/page.tsx",
    "apps/web/app/crm/import/page.tsx",
    "apps/web/app/crm/review/page.tsx",
    "apps/web/app/crm/followups/page.tsx",
    "apps/web/app/crm/reports/page.tsx",
    "apps/web/app/operator/page.tsx",
    "apps/web/app/review-queue/page.tsx",
    "apps/web/app/outreach-lab/page.tsx",
    "apps/web/app/followups/page.tsx",
]

V11_API = [
    "apps/web/app/api/crm/accounts/route.ts",
    "apps/web/app/api/crm/accounts/[id]/route.ts",
    "apps/web/app/api/crm/accounts/[id]/stage/route.ts",
    "apps/web/app/api/crm/accounts/[id]/note/route.ts",
    "apps/web/app/api/crm/accounts/[id]/followup/route.ts",
    "apps/web/app/api/crm/drafts/route.ts",
    "apps/web/app/api/crm/drafts/[id]/approve/route.ts",
    "apps/web/app/api/crm/drafts/[id]/reject/route.ts",
    "apps/web/app/api/crm/reports/route.ts",
    "apps/web/app/api/crm/import/route.ts",
]

V11_COMPONENTS = [
    "apps/web/components/crm/AccountTable.tsx",
    "apps/web/components/crm/PipelineSummary.tsx",
    "apps/web/components/crm/StageBadge.tsx",
    "apps/web/components/crm/ReviewStatusBadge.tsx",
    "apps/web/components/crm/DraftPreview.tsx",
]

V11_DOCS = [
    "docs/auth/V11_ADMIN_ACCESS_BOUNDARY.md",
    "docs/auth/FOUNDER_ONLY_ROUTES.md",
    "docs/auth/PRODUCTION_AUTH_REQUIREMENTS.md",
]


class TestV11(unittest.TestCase):
    def test_pages_exist(self) -> None:
        missing = [p for p in V11_PAGES if not (ROOT / p).exists()]
        self.assertEqual(missing, [], f"missing pages: {missing}")

    def test_api_exists(self) -> None:
        missing = [p for p in V11_API if not (ROOT / p).exists()]
        self.assertEqual(missing, [], f"missing api routes: {missing}")

    def test_components_exist(self) -> None:
        missing = [p for p in V11_COMPONENTS if not (ROOT / p).exists()]
        self.assertEqual(missing, [], f"missing components: {missing}")

    def test_docs_exist(self) -> None:
        missing = [p for p in V11_DOCS if not (ROOT / p).exists()]
        self.assertEqual(missing, [], f"missing docs: {missing}")

    def test_api_routes_have_no_autosend(self) -> None:
        for p in V11_API:
            text = (ROOT / p).read_text(encoding="utf-8").lower()
            for banned in ["fetch('https://api.whatsapp", "twilio.messages.create", "smtp.send"]:
                self.assertNotIn(banned, text, f"banned autosend pattern in {p}")

    def test_crm_lib_demo_safe(self) -> None:
        text = (ROOT / "apps/web/lib/crm/crm.ts").read_text(encoding="utf-8")
        self.assertIn("fallback", text, "crm lib must have fallback behavior for missing files")


if __name__ == "__main__":
    unittest.main()
