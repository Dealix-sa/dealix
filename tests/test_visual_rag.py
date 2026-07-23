from dealix.visual_rag import (
    VisualRAGAdapter,
    VisualRAGJob,
    VisualRAGMode,
    VisualRAGResult,
    VisualRAGSource,
    VisualRAGTile,
    VisualRAGSensitivity,
    attach_visual_evidence_to_proof_pack,
)


def test_visual_rag_defaults_to_disabled() -> None:
    result = VisualRAGAdapter().run(
        VisualRAGJob(
            job_id="test-disabled",
            mode=VisualRAGMode.DISABLED,
            sources=[VisualRAGSource(kind="url", uri="https://example.com")],
            query="example",
        )
    )

    assert result.status == "disabled"
    assert result.tiles == []


def test_visual_rag_blocks_sensitive_hosted_search() -> None:
    result = VisualRAGAdapter().run(
        VisualRAGJob(
            job_id="test-sensitive-hosted",
            mode=VisualRAGMode.HOSTED_SEARCH,
            sources=[VisualRAGSource(kind="url", uri="https://example.com/private")],
            query="pricing table",
            sensitivity=VisualRAGSensitivity.CLIENT_CONFIDENTIAL,
            allow_external_processing=True,
            require_human_approval=False,
        )
    )

    assert result.status == "blocked"
    assert "private_worker" in result.message


def test_visual_rag_public_hosted_search_requires_approval() -> None:
    result = VisualRAGAdapter().run(
        VisualRAGJob(
            job_id="test-public-hosted",
            mode=VisualRAGMode.HOSTED_SEARCH,
            sources=[VisualRAGSource(kind="url", uri="https://example.com/public")],
            query="public table",
            sensitivity=VisualRAGSensitivity.PUBLIC,
            allow_external_processing=True,
            require_human_approval=True,
        )
    )

    assert result.status == "pending_approval"


def test_visual_evidence_attaches_to_proof_pack() -> None:
    proof_pack = {
        "sections": [],
        "governance": {"requires_founder_review_before_external_share": True},
    }
    result = VisualRAGResult(
        job_id="test-proof-pack",
        status="ok",
        mode=VisualRAGMode.SCREENSHOT_ONLY,
        message="Captured 1 tile.",
        tiles=[
            VisualRAGTile(
                tile_id="tile-1",
                source_id="source-1",
                page=1,
                image_path="reports/visual_rag/test/source_1/page.png",
            )
        ],
    )

    updated = attach_visual_evidence_to_proof_pack(proof_pack, result)

    assert updated["visual_evidence_summary"]["tiles"] == 1
    assert updated["governance"]["visual_evidence_requires_review"] is True
    assert updated["sections"][0]["id"] == "visual_evidence_appendix"
    assert updated["sections"][0]["sources"][0]["tile_id"] == "tile-1"
