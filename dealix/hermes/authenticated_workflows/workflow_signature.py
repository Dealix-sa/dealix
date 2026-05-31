"""Combine all attestations into one signed Workflow Trust Object."""

from __future__ import annotations

import hashlib
import hmac
import json
from dataclasses import asdict, dataclass

from .context_attestation import ContextAttestation
from .data_attestation import DataAttestation
from .intent_proof import IntentProof, _secret
from .tool_attestation import ToolAttestation


@dataclass(frozen=True)
class WorkflowTrustObject:
    intent: IntentProof
    context: ContextAttestation
    tool: ToolAttestation
    data: DataAttestation
    signature: str


def _digest(intent: IntentProof, context: ContextAttestation, tool: ToolAttestation, data: DataAttestation) -> bytes:
    payload = {
        "intent": asdict(intent),
        "context": asdict(context),
        "tool": asdict(tool),
        "data": asdict(data),
    }
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=list)
    return raw.encode("utf-8")


def sign_workflow(
    intent: IntentProof,
    context: ContextAttestation,
    tool: ToolAttestation,
    data: DataAttestation,
) -> WorkflowTrustObject:
    """Bundle four attestations into one HMAC-signed Workflow Trust Object."""
    sig = hmac.new(_secret(), _digest(intent, context, tool, data), hashlib.sha256).hexdigest()
    return WorkflowTrustObject(intent=intent, context=context, tool=tool, data=data, signature=sig)


def signature_valid(obj: WorkflowTrustObject) -> bool:
    """Return True when the bundled signature recomputes correctly."""
    expected = hmac.new(_secret(), _digest(obj.intent, obj.context, obj.tool, obj.data), hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, obj.signature)
