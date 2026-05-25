"""Training router."""

from __future__ import annotations

from fastapi import APIRouter

from dealix.hermes.training.workshop_builder import Workshop, build_workshop


router = APIRouter(prefix="/api/v1/hermes/training", tags=["hermes-training"])


@router.post("/workshops")
def workshop(body: Workshop) -> Workshop:
    return build_workshop(
        workshop_id=body.workshop_id,
        title=body.title,
        audience=body.audience,
        learning_outcomes=body.learning_outcomes,
        duration_minutes=body.duration_minutes,
    )
