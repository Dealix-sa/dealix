"""Safety and approval policy for Dealix VisualRAG.

The policy is intentionally conservative. Visual rendering can expose client
materials, screenshots, URLs, and proprietary documents. External processing is
therefore blocked for sensitive material unless the job explicitly uses a
private worker.
"""

from __future__ import annotations

from dataclasses import dataclass

from dealix.visual_rag.contracts import VisualRAGJob, VisualRAGMode, VisualRAGSensitivity


@dataclass(frozen=True)
class VisualRAGPolicyDecision:
    allowed: bool
    reason: str
    warnings: tuple[str, ...] = ()


def evaluate_visual_rag_job(job: VisualRAGJob) -> VisualRAGPolicyDecision:
    """Return whether a VisualRAG job can proceed in its requested mode."""

    if job.mode == VisualRAGMode.DISABLED:
        return VisualRAGPolicyDecision(
            allowed=False,
            reason="VisualRAG is disabled by configuration.",
            warnings=("Enable screenshot_only, hosted_search, or private_worker mode explicitly.",),
        )

    if not job.sources:
        return VisualRAGPolicyDecision(
            allowed=False,
            reason="No visual sources were provided.",
        )

    if job.sensitivity in {
        VisualRAGSensitivity.CLIENT_CONFIDENTIAL,
        VisualRAGSensitivity.REGULATED,
    }:
        if job.mode != VisualRAGMode.PRIVATE_WORKER:
            return VisualRAGPolicyDecision(
                allowed=False,
                reason=(
                    "Sensitive client or regulated material must use private_worker mode; "
                    "hosted or public processing is blocked."
                ),
                warnings=("Use a private Python 3.12 PixelRAG worker or keep the job disabled.",),
            )
        if job.allow_external_processing:
            return VisualRAGPolicyDecision(
                allowed=False,
                reason="External processing cannot be enabled for sensitive private-worker jobs.",
            )

    if job.mode == VisualRAGMode.HOSTED_SEARCH:
        if job.sensitivity != VisualRAGSensitivity.PUBLIC:
            return VisualRAGPolicyDecision(
                allowed=False,
                reason="Hosted visual search is only allowed for public sources.",
            )
        if not job.allow_external_processing:
            return VisualRAGPolicyDecision(
                allowed=False,
                reason="Hosted search requires allow_external_processing=True.",
            )

    if job.retention_days > 90 and job.sensitivity != VisualRAGSensitivity.PUBLIC:
        return VisualRAGPolicyDecision(
            allowed=False,
            reason="Non-public visual evidence retention cannot exceed 90 days without a specific policy.",
        )

    warnings: list[str] = []
    if job.require_human_approval:
        warnings.append("Human approval remains required before external use or proof-pack publication.")

    if job.mode == VisualRAGMode.SCREENSHOT_ONLY:
        warnings.append("Screenshot-only mode captures evidence but does not perform semantic visual retrieval.")

    return VisualRAGPolicyDecision(allowed=True, reason="VisualRAG job is allowed.", warnings=tuple(warnings))
