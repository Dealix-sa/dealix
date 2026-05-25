"""
Hermes Control Plane — السيادة، السياسات، الصلاحيات، الموافقات، الثقة، الـ Audit.

Pipeline ثابت يمر به كل request:

    runtime.run(context, intent, ...)
        → authorization_gate.check
        → policy_enforcement.evaluate
        → sovereignty_gate.classify
        → trust_gate.assess
        → approval_gate.require_if_needed
        → (handed to execution plane)
        → audit_gate.record (always)

أي gate يمكنه: PASS / DENY / HOLD (يفتح approval ticket).
أي gate يكتب AuditEvent عبر `audit_gate`.
"""

from .runtime import HermesRuntime, RuntimeOutcome
from .kill_switch import KillSwitch, KillSwitchState

__all__ = ["HermesRuntime", "KillSwitch", "KillSwitchState", "RuntimeOutcome"]
