"""Ed25519 (or HMAC-fallback) Proof Pack signer — Phase 2.

Non-Negotiable #9: every evidence pack signed and bilingual.
Non-Negotiable #5: signatures tie to content hash so tampering is detected.
"""

from __future__ import annotations

import base64
import os

import pytest

from auto_client_acquisition.proof_os.signer import (
    SignedAsset,
    sign_payload,
    verify_payload,
)


def test_sign_then_verify_roundtrip():
    payload = b"hello dealix proof pack"
    asset = sign_payload(payload, metadata={"locale": "ar"})
    assert verify_payload(payload, asset) is True


def test_signature_detects_tampering():
    payload = b"original proof"
    asset = sign_payload(payload)
    tampered = b"tampered proof "
    assert verify_payload(tampered, asset) is False


def test_signed_asset_contains_content_hash():
    payload = b"deterministic"
    asset = sign_payload(payload)
    import hashlib

    assert asset.content_sha256 == hashlib.sha256(payload).hexdigest()


def test_to_dict_serializable():
    import json

    asset = sign_payload(b"x", metadata={"locale": "en"})
    payload = asset.to_dict()
    json.dumps(payload)
    assert payload["content_sha256"] and payload["signature_b64"] and payload["public_key_b64"]


def test_dev_key_refused_in_production(monkeypatch):
    """Production env MUST refuse the deterministic dev key."""
    monkeypatch.setenv("APP_ENV", "production")
    # core.config.settings is shadowed by an instance in __init__; reach the
    # module via sys.modules to clear the LRU cache cleanly.
    import sys

    settings_mod = sys.modules["core.config.settings"]
    settings_mod.get_settings.cache_clear()
    try:
        with pytest.raises(RuntimeError) as exc:
            sign_payload(b"x")
        assert "dev_key_in_production" in str(exc.value)
    finally:
        monkeypatch.delenv("APP_ENV", raising=False)
        settings_mod.get_settings.cache_clear()


def test_custom_key_accepted(monkeypatch):
    """A non-dev key is accepted even outside production."""
    monkeypatch.setenv("APP_ENV", "development")
    custom_seed = base64.b64encode(b"d" * 32).decode()
    asset = sign_payload(b"x", private_key_b64=custom_seed)
    assert verify_payload(b"x", asset) or asset.algorithm == "hmac-sha256"


def test_signed_asset_immutable():
    asset = sign_payload(b"x")
    with pytest.raises(Exception):
        asset.content_sha256 = "tampered"  # type: ignore[misc]


def test_invalid_key_length_rejected():
    with pytest.raises(ValueError) as exc:
        sign_payload(b"x", private_key_b64=base64.b64encode(b"too_short").decode())
    assert "32 bytes" in str(exc.value)


def test_payload_must_be_bytes():
    with pytest.raises(TypeError):
        sign_payload("a string not bytes")  # type: ignore[arg-type]
