"""Manifest review — owner signature, hash, declared tools, data scope."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ManifestReview:
    passed: bool
    reasons: tuple[str, ...]
    manifest_hash: str


def _hash_manifest(manifest: dict[str, Any]) -> str:
    import json
    canonical = json.dumps(manifest, sort_keys=True).encode()
    return hashlib.sha256(canonical).hexdigest()


def review_manifest(manifest: dict[str, Any]) -> ManifestReview:
    reasons: list[str] = []
    if "owner" not in manifest or not manifest["owner"]:
        reasons.append("missing owner field")
    if "tools" not in manifest or not isinstance(manifest["tools"], list):
        reasons.append("missing or invalid tools list")
    if "data_scope" not in manifest:
        reasons.append("missing data_scope")
    if not manifest.get("signed", False):
        reasons.append("manifest not signed")
    return ManifestReview(
        passed=not reasons,
        reasons=tuple(reasons),
        manifest_hash=_hash_manifest(manifest),
    )
