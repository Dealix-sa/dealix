"""Company Brain — loads founder profile, offers, personas, and shared config.

Single source of truth for the founder's canonical email and the offer ladder.
All data is loaded from ``data/dealix_conversation_negotiation/`` using stdlib
only so the engine never breaks CI.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "data" / "dealix_conversation_negotiation"

CANONICAL_FOUNDER_EMAIL = "sami.assiri11@gmail.com"


def _load_json(name: str) -> Any:
    path = DATA_DIR / name
    if not path.is_file():
        raise FileNotFoundError(f"Missing conversation-engine data file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def founder_profile() -> dict[str, Any]:
    profile = _load_json("founder_profile.json")
    # Hard-enforce the canonical email regardless of file drift.
    profile["canonical_email"] = CANONICAL_FOUNDER_EMAIL
    return profile


@lru_cache(maxsize=1)
def offers() -> list[dict[str, Any]]:
    return list(_load_json("offers.json").get("offers", []))


@lru_cache(maxsize=1)
def personas() -> list[dict[str, Any]]:
    return list(_load_json("personas.json").get("personas", []))


@lru_cache(maxsize=1)
def objections() -> list[dict[str, Any]]:
    return list(_load_json("objections.json").get("objections", []))


@lru_cache(maxsize=1)
def channels() -> dict[str, Any]:
    return dict(_load_json("channels.json").get("channels", {}))


@lru_cache(maxsize=1)
def proof_rules() -> dict[str, Any]:
    return dict(_load_json("proof_rules.json"))


@lru_cache(maxsize=1)
def seed_targets() -> list[dict[str, Any]]:
    return list(_load_json("seed_targets.json").get("targets", []))


def offer_by_id(offer_id: str) -> dict[str, Any] | None:
    for offer in offers():
        if offer.get("id") == offer_id:
            return offer
    return None


def persona_by_id(persona_id: str) -> dict[str, Any] | None:
    for persona in personas():
        if persona.get("id") == persona_id:
            return persona
    return None


def founder_email() -> str:
    return CANONICAL_FOUNDER_EMAIL


def founder_signature(lang: str = "en") -> str:
    profile = founder_profile()
    key = "signature_ar" if lang == "ar" else "signature_en"
    return str(profile.get(key) or f"Sami — Dealix\n{CANONICAL_FOUNDER_EMAIL}")
