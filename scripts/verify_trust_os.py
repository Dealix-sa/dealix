#!/usr/bin/env python3
"""
verify_trust_os.py — assert the Trust OS guarantees hold:

  1. ClaimGuard refuses known-unsafe text.
  2. ApprovalMatrix blocks auto-execute outbound.
  3. SuppressionList filters correctly.
  4. PolicyEngine refuses suppressed-contact actions.
  5. PublicSafety scanner catches an obvious leak.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from dealix.trust.approval_matrix import ApprovalMatrix  # noqa: E402
from dealix.trust.claim_guard import ClaimGuard  # noqa: E402
from dealix.trust.policy_engine import PolicyEngine  # noqa: E402
from dealix.trust.public_safety import is_safe, scan  # noqa: E402
from dealix.trust.suppression import SuppressionList  # noqa: E402


def main() -> int:
    failures: list[str] = []

    guard = ClaimGuard.from_register()
    if guard.is_safe("Our guaranteed 10x ROI partner solution"):
        failures.append("ClaimGuard accepted overclaim text")
    if not guard.is_safe("We help Saudi B2B teams build a ranked outbound pack"):
        failures.append("ClaimGuard rejected safe text")

    matrix = ApprovalMatrix.from_register()
    if not matrix.is_blocked("auto_send_external_outbound"):
        failures.append("ApprovalMatrix did not block 'auto_send_external_outbound'")
    if not matrix.requires_founder("send_outbound_message"):
        failures.append("ApprovalMatrix should require founder for 'send_outbound_message'")

    sup = SuppressionList()
    sup.add("Founder@Example.com")
    if not sup.contains("founder@example.com"):
        failures.append("SuppressionList lookup is not case/space-insensitive")
    if sup.filter(["founder@example.com", "other@example.com"]) != ["other@example.com"]:
        failures.append("SuppressionList.filter returned wrong list")

    engine = PolicyEngine(suppression=sup)
    result = engine.evaluate("send_outbound_message", target_contact="founder@example.com")
    if result.allowed:
        failures.append("PolicyEngine allowed message to suppressed contact")

    findings = scan("Contact me at customer@bank.com.sa or +966 555 123 456")
    if not findings:
        failures.append("public_safety.scan missed obvious PII")
    if not is_safe("Reach the team at hello@example.com"):
        failures.append("public_safety.is_safe should allow example.com (allowlisted)")

    if failures:
        print(f"[FAIL] verify_trust_os: {len(failures)} issues")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("[OK] verify_trust_os: all trust guarantees hold")
    return 0


if __name__ == "__main__":
    sys.exit(main())
