"""Verify the Founder Console v2 internal API layer is in place.

Checked:
- ``api/routers/internal/founder_console.py`` exists and defines every
  required endpoint path.
- ``docs/api/INTERNAL_API_LAYER_V1.md`` exists and is non-trivial.

This is a static check — it does not boot FastAPI. The boot/build check
lives in ``scripts/verify_founder_console_v2.py``.
"""

from __future__ import annotations

from pathlib import Path


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    router = repo / "api" / "routers" / "internal" / "founder_console.py"
    docs = repo / "docs" / "api" / "INTERNAL_API_LAYER_V1.md"

    failures: list[str] = []

    if not router.exists():
        failures.append("Missing api/routers/internal/founder_console.py")
    else:
        text = router.read_text(encoding="utf-8", errors="ignore")
        required = [
            "/ceo/summary",
            "/sales/funnel",
            "/approvals",
            "/workers/health",
            "/trust/flags",
            "/finance/summary",
            "/distribution/summary",
            "/delivery/queue",
            "/retention/queue",
            "/proof/library",
        ]
        for item in required:
            if item not in text:
                failures.append(f"Router missing endpoint: {item}")

    if not docs.exists() or docs.stat().st_size < 100:
        failures.append("Missing or too small docs/api/INTERNAL_API_LAYER_V1.md")

    if failures:
        print("Internal API layer verification failed:")
        for failure in failures:
            print("-", failure)
        return 1
    print("PASS: internal API layer exists.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
