#!/usr/bin/env python3
"""System health check — verify all founder execution infrastructure is operational."""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIR = ROOT / "company" / "runtime"


class HealthCheck:
    def __init__(self):
        self.checks = []
        self.passed = 0
        self.failed = 0
        self.warnings = 0

    def check(self, name: str, condition: bool, details: str = "") -> None:
        """Log a single health check result."""
        status = "✅" if condition else "❌"
        self.checks.append({"name": name, "status": status, "passed": condition, "details": details})
        if condition:
            self.passed += 1
        else:
            self.failed += 1
        print(f"  {status} {name}")
        if details:
            print(f"     {details}")

    def warn(self, name: str, details: str = "") -> None:
        """Log a warning (not critical, but should be addressed)."""
        self.checks.append({"name": name, "status": "⚠️", "passed": None, "details": details})
        self.warnings += 1
        print(f"  ⚠️  {name}")
        if details:
            print(f"     {details}")

    def summary(self) -> int:
        """Print summary and return exit code."""
        print("")
        print("=" * 50)
        print("Health Check Summary")
        print(f"  ✅ Passed: {self.passed}")
        print(f"  ❌ Failed: {self.failed}")
        print(f"  ⚠️  Warnings: {self.warnings}")
        print("=" * 50)
        print("")

        if self.failed == 0:
            print("🎉 All critical systems operational! Ready for founder execution.")
            return 0
        else:
            print(f"⚠️  {self.failed} critical issues found. Fix before starting.")
            return 1


def main() -> int:
    print("🔍 Dealix Founder System Health Check")
    print("=" * 50)
    print("")

    hc = HealthCheck()

    # 1. Module Imports
    print("1️⃣  Module Imports:")
    try:
        from company.leads import real_leads_engine
        hc.check("real_leads_engine importable", True)
    except ImportError as e:
        hc.check("real_leads_engine importable", False, str(e))

    try:
        from company.sales import lead_qualification_engine
        hc.check("lead_qualification_engine importable", True)
    except ImportError as e:
        hc.check("lead_qualification_engine importable", False, str(e))

    try:
        from company.sales import sales_qualification_agent
        hc.check("sales_qualification_agent importable", True)
    except ImportError as e:
        hc.check("sales_qualification_agent importable", False, str(e))

    try:
        from company.delivery import pilot_delivery_orchestrator
        hc.check("pilot_delivery_orchestrator importable", True)
    except ImportError as e:
        hc.check("pilot_delivery_orchestrator importable", False, str(e))

    print("")

    # 2. File Structure
    print("2️⃣  Directory Structure:")
    hc.check("company/leads/ exists", (ROOT / "company" / "leads").is_dir())
    hc.check("company/sales/ exists", (ROOT / "company" / "sales").is_dir())
    hc.check("company/delivery/ exists", (ROOT / "company" / "delivery").is_dir())
    hc.check("company/runtime/ exists", (ROOT / "company" / "runtime").is_dir())
    hc.check("scripts/ exists", (ROOT / "scripts").is_dir())

    print("")

    # 3. Critical Scripts
    print("3️⃣  Critical Scripts:")
    hc.check("dealix_founder_daily_complete.sh exists", (ROOT / "scripts" / "dealix_founder_daily_complete.sh").exists())
    hc.check("dealix_founder_daily_complete.sh executable", os.access(ROOT / "scripts" / "dealix_founder_daily_complete.sh", os.X_OK))
    hc.check("generate_founder_dashboard.py exists", (ROOT / "scripts" / "generate_founder_dashboard.py").exists())
    hc.check("generate_approvals_queue.py exists", (ROOT / "scripts" / "generate_approvals_queue.py").exists())

    print("")

    # 4. Documentation
    print("4️⃣  Documentation:")
    docs = [
        ("FOUNDER_DAILY_EXECUTION_PLAYBOOK.md", "Daily ritual instructions"),
        ("FOUNDER_REVENUE_MANUAL.md", "90-day revenue strategy"),
        ("FOUNDER_SYSTEM_OVERVIEW.md", "System architecture & usage"),
        ("PILOT_DAY1_ONBOARDING.md", "Customer onboarding checklist"),
    ]

    for doc, desc in docs:
        path = ROOT / "docs" / doc
        hc.check(f"{doc}", path.exists(), desc)

    print("")

    # 5. Runtime Data
    print("5️⃣  Runtime Data Structure:")
    hc.check("runtime/warm_intro_targets.csv exists", (RUNTIME_DIR / "warm_intro_targets.csv").exists(), "Prospect pipeline tracking")
    hc.check("runtime/founder_dashboard.html generated", (RUNTIME_DIR / "founder_dashboard.html").exists(), "Daily metrics dashboard")
    hc.check("runtime/decisions.html generated", (RUNTIME_DIR / "decisions.html").exists(), "Approvals queue UI")

    print("")

    # 6. Environment
    print("6️⃣  Environment Configuration:")
    google_key = os.getenv("GOOGLE_MAPS_API_KEY")
    hc.check("GOOGLE_MAPS_API_KEY set", bool(google_key), "Required for lead research" if not google_key else f"Key present (length: {len(google_key)})")

    moyasar_key = os.getenv("MOYASAR_API_KEY")
    hc.warn("MOYASAR_API_KEY set", "Payment processing (optional for testing)" if not moyasar_key else "Key present")

    whatsapp_key = os.getenv("WHATSAPP_API_KEY")
    hc.warn("WHATSAPP_API_KEY set", "WhatsApp automation (optional for now)" if not whatsapp_key else "Key present")

    print("")

    # 7. Dependencies
    print("7️⃣  Python Dependencies:")
    required = ["csv", "json", "pathlib"]
    for lib in required:
        try:
            __import__(lib)
            hc.check(f"{lib} available", True)
        except ImportError:
            hc.check(f"{lib} available", False, "Not installed")

    print("")

    # 8. System Integration Tests
    print("8️⃣  Integration Tests:")

    # Test: Can generate founder dashboard?
    try:
        from company.leads.real_leads_engine import score as real_leads_score
        test_row = {"phone": "+966501234567", "website": "test.com"}
        score = real_leads_score(test_row)
        hc.check("real_leads scoring works", score >= 45, f"Test score: {score}")
    except Exception as e:
        hc.check("real_leads scoring works", False, str(e))

    # Test: Can generate sales qualifications?
    try:
        from company.sales.sales_qualification_agent import generate_bant_assessment
        bant = generate_bant_assessment("Test diagnostic notes")
        hc.check("BANT assessment generation works", bant.get("total_bant_score") is not None, f"Test BANT score: {bant.get('total_bant_score')}")
    except Exception as e:
        hc.check("BANT assessment generation works", False, str(e))

    # Test: Can generate pilot projects?
    try:
        from company.delivery.pilot_delivery_orchestrator import generate_pilot_contract
        contract = generate_pilot_contract("Test", "Test Co", "2026-06-17")
        hc.check("Pilot contract generation works", contract.get("contract_id") is not None, f"Test contract ID: {contract.get('contract_id')}")
    except Exception as e:
        hc.check("Pilot contract generation works", False, str(e))

    print("")

    # 9. Recommendations
    print("9️⃣  Recommendations:")

    if not google_key:
        hc.warn("Add GOOGLE_MAPS_API_KEY", "Get from Google Cloud Console → APIs & Services → Credentials")

    log_file = RUNTIME_DIR / f"daily_ritual_{datetime.now().isoformat()[:10]}.log"
    if not log_file.exists():
        hc.warn("Run daily ritual at least once", "Execute: bash scripts/dealix_founder_daily_complete.sh")

    print("")

    # Final Summary
    return hc.summary()


if __name__ == '__main__':
    sys.exit(main())
