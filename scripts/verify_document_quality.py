"""Verify that every operating .md document meets the Dealix Document Standard.

Fails the build if any document in the operating doc tree is missing required
sections or is suspiciously short. Documented in `docs/ops/DOCUMENT_STANDARD.md`.
"""

from pathlib import Path

REQUIRED_SECTIONS = [
    "## Purpose",
    "## Owner",
    "## Review Cadence",
    "## Inputs",
    "## Outputs",
    "## Rules",
    "## Metrics",
    "## Evidence",
]

DOC_FOLDERS = [
    "docs/founder",
    "docs/strategy",
    "docs/revenue",
    "docs/acquisition",
    "docs/sales",
    "docs/delivery",
    "docs/trust",
    "docs/finance",
    "docs/client_success",
    "docs/product",
    "docs/content",
    "docs/learning",
    "docs/people",
    "docs/agents",
    "docs/ai_management",
    "docs/control_plane",
    "docs/ops",
]

SKIP_FILES = {
    "README.md",
}


def main() -> int:
    failures: list[str] = []

    for folder in DOC_FOLDERS:
        base = Path(folder)
        if not base.exists():
            failures.append(f"Missing folder: {folder}")
            continue

        for path in base.rglob("*.md"):
            if path.name in SKIP_FILES:
                continue

            text = path.read_text(encoding="utf-8", errors="ignore")

            if path.stat().st_size < 120:
                failures.append(f"Too short: {path}")
                continue

            missing_sections = [
                section for section in REQUIRED_SECTIONS if section not in text
            ]

            if missing_sections:
                failures.append(
                    f"{path} missing sections: {', '.join(missing_sections)}"
                )

    if failures:
        print("Document quality failures:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS: all operating documents meet Dealix document standard.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
