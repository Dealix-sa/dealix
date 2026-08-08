"""Verify that the codebase is ready for controlled-live outbound activation.

Checks:
1. Policy gate exists and enforces all required gates
2. Consent, suppression, and rate-limit modules are importable
3. Blocked claims list is populated
4. Safety invariants in Company Intelligence are intact
5. No hardcoded EXTERNAL_SEND_ENABLED=true in source code

Exit 0 = READY, exit 1 = NOT READY.
"""
from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))

PASS = 0
FAIL = 0


def check(label: str, condition: bool, detail: str = "") -> None:
    global PASS, FAIL  # noqa: PLW0603
    if condition:
        PASS += 1
        print(f"  ✅ {label}")
    else:
        FAIL += 1
        msg = f"  ❌ {label}"
        if detail:
            msg += f" — {detail}"
        print(msg)


print("=== Controlled-Live Outbound Readiness ===\n")

# 1. Policy gate module
print("[1] Policy gate")
try:
    from app.outbound.policy_gate import (
        BLOCKED_CLAIMS,
        CHANNELS,
        GateResult,
        SendEvaluation,
        can_send_email,
        can_send_whatsapp,
        default_safety_status,
        evaluate_channel_send,
        evaluate_email_send,
        evaluate_sms_send,
        evaluate_whatsapp_send,
        get_outbound_mode,
        is_external_send_enabled,
    )

    check("policy_gate imports", True)
except ImportError as e:
    check("policy_gate imports", False, str(e))

# 2. Defaults are fail-closed
print("\n[2] Fail-closed defaults")
safe_env: dict[str, str] = {}  # empty env = all disabled
check(
    "EXTERNAL_SEND_ENABLED defaults false",
    not is_external_send_enabled(safe_env),
)
check(
    "OUTBOUND_MODE defaults draft_only",
    get_outbound_mode(safe_env) == "draft_only",
)
status = default_safety_status(safe_env)
check("safe_to_send defaults false", status["safe_to_send"] is False)
check("email_send_enabled defaults false", status["email_send_enabled"] is False)
check("whatsapp_send_enabled defaults false", status["whatsapp_send_enabled"] is False)
check("sms_send_enabled defaults false", status["sms_send_enabled"] is False)

# 3. Blocked claims
print("\n[3] Content safety")
check("blocked_claims populated", len(BLOCKED_CLAIMS) >= 5)
check("'guaranteed roi' in blocked", "guaranteed roi" in BLOCKED_CLAIMS)
check("'مضمون' in blocked", "مضمون" in BLOCKED_CLAIMS)

# 4. Cross-cutting guards importable
print("\n[4] Cross-cutting guards")
for mod_name in [
    "app.outbound.consent",
    "app.outbound.rate_limiter",
    "app.outbound.suppression",
]:
    try:
        importlib.import_module(mod_name)
        check(f"{mod_name} importable", True)
    except ImportError as e:
        check(f"{mod_name} importable", False, str(e))

# 5. Channels
print("\n[5] Channel coverage")
check("email channel", "email" in CHANNELS)
check("whatsapp channel", "whatsapp" in CHANNELS)
check("sms channel", "sms" in CHANNELS)

# 6. Evaluate API works in draft mode
print("\n[6] Draft-mode evaluation (no env vars)")
eval_result = evaluate_email_send(
    message={"status": "approved", "body": "test opt-out إيقاف"},
    contact={
        "email": "test@example.com",
        "verification_status": "approved_to_send",
        "source_url": "https://example.com",
    },
    env={},  # all disabled
)
check("email blocked in draft mode", not eval_result.safe_to_send)
check("mode is draft_only", eval_result.mode == "draft_only")

# 7. Company Intelligence safety
print("\n[7] Company Intelligence safety invariants")
try:
    from dealix.company_intelligence.daily_command_engine import (
        DailyCommandBrief,
        DailyHealthAssessment,
    )
    from datetime import date

    try:
        DailyCommandBrief(
            tenant_id="test",
            brief_id="test",
            brief_date=date.today(),
            health=DailyHealthAssessment(),
            execution_allowed=True,
            source_id="test",
        )
        check("execution_allowed=True rejected", False, "should have raised")
    except ValueError:
        check("execution_allowed=True rejected", True)
except ImportError as e:
    check("company intelligence import", False, str(e))

try:
    from dealix.company_intelligence.pipeline_engine import RevenueForecast

    try:
        RevenueForecast(
            tenant_id="test",
            forecast_id="test",
            forecast_period="q1",
            recognized_revenue=True,
            source_id="test",
        )
        check("recognized_revenue=True rejected", False, "should have raised")
    except ValueError:
        check("recognized_revenue=True rejected", True)
except ImportError as e:
    check("pipeline engine import", False, str(e))

# 8. No hardcoded EXTERNAL_SEND_ENABLED=true in source
print("\n[8] No hardcoded live-send in source code")
dangerous_patterns = [
    'EXTERNAL_SEND_ENABLED=true',
    'EXTERNAL_SEND_ENABLED="true"',
    "EXTERNAL_SEND_ENABLED='true'",
]
source_dirs = [ROOT / "api", ROOT / "app", ROOT / "core", ROOT / "dealix"]
found_hardcoded = False
for d in source_dirs:
    if not d.exists():
        continue
    for py in d.rglob("*.py"):
        content = py.read_text(errors="ignore")
        for line_num, line in enumerate(content.splitlines(), 1):
            stripped = line.strip()
            # Skip comments and docstrings
            if stripped.startswith("#") or stripped.startswith('"""') or stripped.startswith("'''"):
                continue
            for pat in dangerous_patterns:
                if pat in line:
                    check(
                        f"no hardcoded {pat}",
                        False,
                        f"found in {py.relative_to(ROOT)}:{line_num}",
                    )
                    found_hardcoded = True
if not found_hardcoded:
    check("no hardcoded EXTERNAL_SEND_ENABLED=true", True)

# Summary
print(f"\n{'='*50}")
if FAIL == 0:
    print(f"CONTROLLED_LIVE_READINESS=READY ({PASS} checks passed)")
    sys.exit(0)
else:
    print(f"CONTROLLED_LIVE_READINESS=NOT_READY ({FAIL} failed, {PASS} passed)")
    sys.exit(1)
