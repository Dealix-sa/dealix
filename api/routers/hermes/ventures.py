"""Ventures router."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from dealix.hermes.ventures.kill_scale import evaluate_vertical
from dealix.hermes.ventures.vertical_launcher import VerticalCard, launch_vertical


router = APIRouter(prefix="/api/v1/hermes/ventures", tags=["hermes-ventures"])


@router.post("/launch")
def launch(body: VerticalCard):
    try:
        return launch_vertical(body)
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc


@router.get("/evaluate")
def evaluate(paid_pilots: int, qualified_replies: int, days_since_launch: int):
    return {"verdict": evaluate_vertical(
        paid_pilots=paid_pilots,
        qualified_replies=qualified_replies,
        days_since_launch=days_since_launch,
    ).value}
