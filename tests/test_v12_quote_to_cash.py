"""Tests for V12 quote-to-cash + deal desk."""

from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


V12_FILES = [
    "business/_data/deals.ledger.json",
    "business/_data/quotes.index.json",
    "business/_data/invoices.index.json",
    "business/_schemas/deal.schema.json",
    "business/_schemas/quote.schema.json",
    "business/_schemas/invoice.schema.json",
    "scripts/lib/quote_engine.py",
    "scripts/generate_quote.py",
    "scripts/review_quote.py",
    "scripts/approve_quote.py",
    "scripts/mark_quote_sent.py",
    "scripts/generate_invoice_stub.py",
    "scripts/generate_revenue_report.py",
    "business/deal-desk/DEAL_DESK_RULES.md",
    "business/deal-desk/QUOTE_APPROVAL_POLICY.md",
    "business/deal-desk/PRICING_DISCOUNT_POLICY.md",
    "business/deal-desk/CHANGE_REQUEST_POLICY.md",
    "business/deal-desk/CONTRACT_HANDOFF_CHECKLIST.md",
    "business/deal-desk/RED_FLAGS_AND_DISQUALIFICATION.md",
    "business/deal-desk/LEGAL_REVIEW_TRIGGERS.md",
    "business/contracts/MASTER_SERVICE_AGREEMENT_OUTLINE.md",
    "business/contracts/STATEMENT_OF_WORK_TEMPLATE_AR.md",
    "business/contracts/STATEMENT_OF_WORK_TEMPLATE_EN.md",
    "business/contracts/DATA_PROCESSING_ADDENDUM_OUTLINE.md",
    "business/contracts/ACCEPTANCE_CRITERIA_TEMPLATE.md",
    "business/contracts/CLIENT_RESPONSIBILITIES.md",
    "apps/web/lib/finance/deals.ts",
    "apps/web/app/deals/page.tsx",
    "apps/web/app/quotes/page.tsx",
    "apps/web/app/revenue/page.tsx",
    "docs/payments/PAYMENT_ARCHITECTURE.md",
    "docs/payments/MOYASAR_INTEGRATION_PLAN.md",
    "docs/payments/STRIPE_INTEGRATION_PLAN.md",
    "docs/payments/ZATCA_AWARE_INVOICING_NOTES.md",
    "docs/payments/PAYMENT_SECURITY_BOUNDARIES.md",
    "integrations/payments/__init__.py",
    "integrations/payments/base.py",
    "integrations/payments/moyasar_stub.py",
    "integrations/payments/stripe_stub.py",
]


class TestV12(unittest.TestCase):
    def test_files_exist(self) -> None:
        missing = [p for p in V12_FILES if not (ROOT / p).exists()]
        self.assertEqual(missing, [], f"missing: {missing}")

    def test_payment_stubs_raise_when_called(self) -> None:
        import sys
        sys.path.insert(0, str(ROOT))
        from integrations.payments.base import PaymentLinkRequest, StubNotActivated
        from integrations.payments.moyasar_stub import MoyasarStub
        from integrations.payments.stripe_stub import StripeStub

        req = PaymentLinkRequest(quote_id="Q-x", amount=100, currency="SAR", customer_name="x", description="x")
        for prov in (MoyasarStub(), StripeStub()):
            with self.assertRaises(StubNotActivated):
                prov.create_payment_link(req)

    def test_quote_generator_writes_index_and_doc(self) -> None:
        # Use a temp working space by snapshotting/restoring the index
        index_path = ROOT / "business/_data/quotes.index.json"
        before = json.loads(index_path.read_text(encoding="utf-8"))
        before_count = len(before["quotes"])
        try:
            out = subprocess.run(
                ["python3", str(ROOT / "scripts/generate_quote.py"),
                 "--account-id", "demo-acc-001",
                 "--offer", "Revenue OS",
                 "--setup-price", "15000",
                 "--monthly-price", "5000"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                timeout=20,
            )
            self.assertEqual(out.returncode, 0, msg=out.stderr)
            after = json.loads(index_path.read_text(encoding="utf-8"))
            self.assertEqual(len(after["quotes"]), before_count + 1)
            self.assertEqual(after["quotes"][-1]["status"], "pending_review")
            self.assertTrue(after["quotes"][-1]["demo"])
        finally:
            index_path.write_text(json.dumps(before, indent=2, ensure_ascii=False), encoding="utf-8")

    def test_no_guaranteed_in_contracts(self) -> None:
        for p in V12_FILES:
            if p.startswith("business/contracts/") or p.startswith("business/deal-desk/"):
                text = (ROOT / p).read_text(encoding="utf-8").lower()
                for banned in ["guaranteed roi", "نضمن نتائج", "100% money-back guarantee"]:
                    self.assertNotIn(banned, text, f"banned phrase in {p}: {banned}")


if __name__ == "__main__":
    unittest.main()
