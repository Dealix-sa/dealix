"""
Security — defense-in-depth against prompt injection, data exfiltration,
and hallucinated claims.

Compose order at runtime:

1. context isolation
2. data classification (already in `dealix.classifications`)
3. prompt sanitization (`agent_comms.message_sanitizer`)
4. tool permissioning (`identity.capability_scope` + `mcp.gateway`)
5. output validation (this package)
6. human approval (`dealix.governance.approvals`)
7. audit trails (`dealix.trust.audit`)
8. kill switch (`mcp.kill_switch`)
9. incident response (`security.red_team` playbooks)
"""

from __future__ import annotations

from dealix.hermes.security.claim_verifier import (
    ClaimVerification,
    verify_claims,
)
from dealix.hermes.security.data_loss_prevention import (
    DLPVerdict,
    scan_for_data_loss,
)
from dealix.hermes.security.indirect_injection_detector import (
    IndirectInjectionVerdict,
    detect_indirect_injection,
)
from dealix.hermes.security.instruction_data_separator import (
    SeparatedPrompt,
    separate_instructions_from_data,
)
from dealix.hermes.security.output_sanitizer import (
    OutputSanitization,
    sanitize_output,
)
from dealix.hermes.security.prompt_injection_tests import (
    PROMPT_INJECTION_TEST_VECTORS,
    PromptInjectionTestVector,
)
from dealix.hermes.security.red_team import (
    RED_TEAM_PLAYBOOKS,
    RedTeamPlaybook,
)

__all__ = [
    "ClaimVerification",
    "verify_claims",
    "DLPVerdict",
    "scan_for_data_loss",
    "IndirectInjectionVerdict",
    "detect_indirect_injection",
    "SeparatedPrompt",
    "separate_instructions_from_data",
    "OutputSanitization",
    "sanitize_output",
    "PROMPT_INJECTION_TEST_VECTORS",
    "PromptInjectionTestVector",
    "RED_TEAM_PLAYBOOKS",
    "RedTeamPlaybook",
]
