#!/usr/bin/env python3
"""Verify the local LiteLLM/OpenAI-compatible gateway for Dealix.

This script is intentionally dependency-light: it uses only Python stdlib.
It checks:
1. /models is reachable with the configured bearer token.
2. Expected Dealix model aliases are exposed.
3. A tiny chat completion succeeds unless --skip-chat is passed.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any


EXPECTED_MODELS = ("dealix-code", "dealix-smart", "dealix-fast")


def _request(method: str, url: str, bearer_token: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = None
    headers = {"Authorization": f"Bearer {bearer_token}"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{method} {url} failed with HTTP {exc.code}: {body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"{method} {url} failed: {exc.reason}") from exc


def _model_ids(models_payload: dict[str, Any]) -> set[str]:
    data = models_payload.get("data", [])
    ids: set[str] = set()
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict) and item.get("id"):
                ids.add(str(item["id"]))
    return ids


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify Dealix local AI gateway")
    parser.add_argument("--base-url", default=os.getenv("OPENAI_API_BASE", "http://localhost:4000/v1"))
    parser.add_argument("--token", default=os.getenv("LITELLM_MASTER_KEY") or os.getenv("OPENAI_API_KEY", ""))
    parser.add_argument("--model", default="dealix-code")
    parser.add_argument("--skip-chat", action="store_true")
    args = parser.parse_args()

    if not args.token:
        print("ERROR: missing --token, LITELLM_MASTER_KEY, or OPENAI_API_KEY", file=sys.stderr)
        return 2

    base_url = args.base_url.rstrip("/")
    print(f"Checking models at {base_url}/models")
    models_payload = _request("GET", f"{base_url}/models", args.token)
    ids = _model_ids(models_payload)
    print("Models:", ", ".join(sorted(ids)) or "(none)")

    missing = [model for model in EXPECTED_MODELS if model not in ids]
    if missing:
        print("WARNING: expected Dealix aliases missing:", ", ".join(missing), file=sys.stderr)

    if not args.skip_chat:
        print(f"Checking chat completion with model={args.model}")
        response = _request(
            "POST",
            f"{base_url}/chat/completions",
            args.token,
            {
                "model": args.model,
                "messages": [
                    {
                        "role": "user",
                        "content": "Reply with exactly: DEALIX_AI_GATEWAY_OK",
                    }
                ],
                "temperature": 0,
                "max_tokens": 32,
            },
        )
        message = (
            response.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
        )
        print("Response:", message.strip())

    print("DEALIX_AI_GATEWAY_VERIFY_DONE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
