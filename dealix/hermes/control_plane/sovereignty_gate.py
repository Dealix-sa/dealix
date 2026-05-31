"""
Sovereignty Gate — يلفّ `sovereignty.classify` ويحوّله إلى `GateResult`.
الفصل بين `sovereignty.py` (الوظيفة الصرفة) و `sovereignty_gate.py` (الـ wrapper
للـ runtime) متعمَّد: يخلي الـ classifier قابلًا للاختبار بدون runtime، ويخلي
الـ runtime يستهلك واجهة gates موحّدة.
"""

from __future__ import annotations

from typing import Any

from ..contracts import ContextPacket, GateResult
from ..sovereignty import classify


class SovereigntyGate:
    STAGE = "gate.sovereignty"

    def assess(
        self,
        context: ContextPacket,
        intent: str,
        extra_signals: dict[str, Any] | None = None,
    ) -> GateResult:
        decision = classify(
            context=context, intent=intent, extra_signals=extra_signals
        )
        passed = decision.sovereignty_level.value != "S5_BLOCKED"
        return GateResult(
            stage=self.STAGE,
            passed=passed,
            sovereignty_override=decision.sovereignty_level,
            approval_required=decision.approval_required,
            reason=(
                None if passed else f"intent `{intent}` is hard-blocked (S5)"
            ),
            metadata={
                "risk_level": decision.risk_level.value,
                "reasons": decision.reasons,
            },
        )


__all__ = ["SovereigntyGate"]
