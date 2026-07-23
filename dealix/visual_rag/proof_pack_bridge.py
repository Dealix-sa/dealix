"""Bridge VisualRAG evidence into Dealix proof-pack drafts.

This module only converts approved visual retrieval results into structured
source references. It does not call PixelRAG, send content, or publish client
materials.
"""

from typing import Any

from dealix.visual_rag.contracts import VisualRAGResult, VisualRAGTile


VISUAL_EVIDENCE_SECTION_ID = "visual_evidence_appendix"


def visual_tile_to_source(tile: VisualRAGTile) -> dict[str, Any]:
    """Convert a VisualRAG tile into a proof-pack source reference."""

    return {
        "type": "visual_tile",
        "tile_id": tile.tile_id,
        "source_id": tile.source_id,
        "page": tile.page,
        "score": tile.score,
        "image_path": tile.image_path,
        "image_url": tile.image_url,
        "snippet": tile.snippet,
        "metadata": tile.metadata,
        "requires_human_review": True,
    }


def build_visual_evidence_section(result: VisualRAGResult) -> dict[str, Any]:
    """Build a proof-pack appendix section from a VisualRAG result."""

    sources = [visual_tile_to_source(tile) for tile in result.tiles]
    status = "ready_for_review" if result.status == "ok" and sources else "pending_visual_evidence"

    return {
        "id": VISUAL_EVIDENCE_SECTION_ID,
        "title_ar": "ملحق الأدلة المرئية",
        "title_en": "Visual Evidence Appendix",
        "body_ar": "أدلة مرئية من صفحات أو مستندات داعمة وتحتاج مراجعة بشرية قبل التسليم.",
        "body_en": "Visual evidence from supporting pages or documents; review is required before delivery.",
        "sources": sources,
        "is_estimate": False,
        "status": status,
        "visual_rag": {
            "job_id": result.job_id,
            "mode": result.mode.value,
            "status": result.status,
            "message": result.message,
            "warnings": result.warnings,
            "next_actions": result.next_actions,
        },
    }


def attach_visual_evidence_to_proof_pack(
    proof_pack: dict[str, Any],
    result: VisualRAGResult,
) -> dict[str, Any]:
    """Return a proof-pack draft with a visual evidence appendix attached."""

    updated = dict(proof_pack)
    sections = [dict(section) for section in updated.get("sections", [])]
    visual_section = build_visual_evidence_section(result)

    replaced = False
    for index, section in enumerate(sections):
        if section.get("id") == VISUAL_EVIDENCE_SECTION_ID:
            sections[index] = visual_section
            replaced = True
            break
    if not replaced:
        sections.append(visual_section)

    governance = dict(updated.get("governance", {}))
    governance.update(
        {
            "visual_evidence_requires_review": True,
            "visual_evidence_approval_first": True,
        }
    )

    updated["sections"] = sections
    updated["governance"] = governance
    updated["visual_evidence_summary"] = {
        "job_id": result.job_id,
        "status": result.status,
        "mode": result.mode.value,
        "tiles": len(result.tiles),
        "warnings": result.warnings,
    }
    return updated
