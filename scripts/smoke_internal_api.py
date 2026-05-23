#!/usr/bin/env python3
"""Probe the local Dealix internal API (/api/v1/internal/ceo/summary).

Behavior:
- If the server is not running on http://127.0.0.1:8000, prints "server not
  running, skipped" and exits 0 (so CI can run this safely without a server).
- If reachable, sends the X-Dealix-Internal-Token header (from the env var
  DEALIX_INTERNAL_TOKEN), prints the HTTP status, and exits 0 on any HTTP
  response (this is a smoke probe, not an assertion).
"""

from __future__ import annotations

import os
import socket
import sys
from typing import Tuple

URL = "http://127.0.0.1:8000/api/v1/internal/ceo/summary"
HOST = "127.0.0.1"
PORT = 8000
TIMEOUT_SECONDS = 3.0


def server_listening(host: str, port: int) -> bool:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1.0)
    try:
        sock.connect((host, port))
        return True
    except OSError:
        return False
    finally:
        sock.close()


def fetch_with_httpx(url: str, headers: dict) -> Tuple[int, str]:
    import httpx  # type: ignore

    with httpx.Client(timeout=TIMEOUT_SECONDS) as client:
        response = client.get(url, headers=headers)
    return response.status_code, response.text[:300]


def fetch_with_urllib(url: str, headers: dict) -> Tuple[int, str]:
    import urllib.error
    import urllib.request

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
            return resp.status, resp.read(300).decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        body = exc.read(300).decode("utf-8", errors="replace") if hasattr(exc, "read") else ""
        return exc.code, body


def main() -> int:
    print("Dealix internal-API smoke probe")
    print("-" * 40)
    if not server_listening(HOST, PORT):
        print(f"  server not listening on {HOST}:{PORT}; skipped")
        print("summary: SKIPPED (exit 0)")
        return 0

    token = os.environ.get("DEALIX_INTERNAL_TOKEN", "")
    headers = {"X-Dealix-Internal-Token": token} if token else {}
    if not token:
        print("  DEALIX_INTERNAL_TOKEN not set; sending without token (dev mode probe)")
    try:
        status, body = fetch_with_httpx(URL, headers)
    except Exception:
        status, body = fetch_with_urllib(URL, headers)
    print(f"  GET {URL}")
    print(f"  status: {status}")
    print(f"  body (first 300 chars): {body!r}")
    print("summary: PROBED (exit 0)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
