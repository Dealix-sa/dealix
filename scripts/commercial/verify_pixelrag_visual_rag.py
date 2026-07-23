#!/usr/bin/env python3
"""Verify the Dealix PixelRAG integration boundary stays production-safe.

This script intentionally does not require PixelRAG to be installed. It verifies
that the adapter exists, defaults to disabled, blocks sensitive hosted jobs, and
keeps PixelRAG optional for Dealix CI/Railway.
"""

from dealix.visual_rag import (
    VisualRAGAdapter,
    VisualRAGJob,
    VisualRAGMode,
    VisualRAGSensitivity,
    VisualRAGSource,
)


def main() -> int:
    adapter = VisualRAGAdapter()

    disabled = adapter.run(
        VisualRAGJob(
            job_id="verify-disabled",
            mode=VisualRAGMode.DISABLED,
            sources=[VisualRAGSource(kind="url", uri="https://example.com", title="Example")],
            query="example",
        )
    )
    assert disabled.status == "disabled", disabled

    sensitive_hosted = adapter.run(
        VisualRAGJob(
            job_id="verify-sensitive-hosted-blocked",
            mode=VisualRAGMode.HOSTED_SEARCH,
            sources=[VisualRAGSource(kind="url", uri="https://example.com/private.pdf")],
            query="pricing table",
            sensitivity=VisualRAGSensitivity.CLIENT_CONFIDENTIAL,
            allow_external_processing=True,
            require_human_approval=False,
        )
    )
    assert sensitive_hosted.status == "blocked", sensitive_hosted

    public_pending_approval = adapter.run(
        VisualRAGJob(
            job_id="verify-public-pending-approval",
            mode=VisualRAGMode.HOSTED_SEARCH,
            sources=[VisualRAGSource(kind="url", uri="https://example.com/public")],
            query="public table",
            sensitivity=VisualRAGSensitivity.PUBLIC,
            allow_external_processing=True,
            require_human_approval=True,
        )
    )
    assert public_pending_approval.status == "pending_approval", public_pending_approval

    print("OK: PixelRAG VisualRAG adapter is optional, policy-gated, and production-safe.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
