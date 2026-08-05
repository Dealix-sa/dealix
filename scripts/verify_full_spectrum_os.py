"""Verify that the Dealix full-spectrum operating system files exist.

Each Command Center is a lightweight governance file. They are mandatory
because the operating system relies on every layer (revenue, trust,
delivery, learning, finance, client success, productization, AI
governance, content, partners, people) being documented before scale.
"""

from pathlib import Path

REQUIRED = [
    "docs/revenue/REVENUE_COMMAND_CENTER.md",
    "docs/trust/TRUST_COMMAND_CENTER.md",
    "docs/delivery/revenue_sprint/REVENUE_SPRINT_FACTORY.md",
    "docs/learning/LEARNING_COMMAND_CENTER.md",
    "docs/finance/FINANCE_COMMAND_CENTER.md",
    "docs/client_success/CLIENT_SUCCESS_COMMAND_CENTER.md",
    "docs/product/PRODUCTIZATION_COMMAND_CENTER.md",
    "docs/ai_management/AI_COMMAND_CENTER.md",
    "docs/content/CONTENT_COMMAND_CENTER.md",
    "docs/partners/PARTNER_COMMAND_CENTER.md",
    "docs/people/DELEGATION_COMMAND_CENTER.md",
]

MIN_BYTES = 250


def main() -> int:
    failures: list[str] = []
    for relpath in REQUIRED:
        path = Path(relpath)
        if not path.exists():
            failures.append(f"Missing: {relpath}")
            continue
        if path.stat().st_size < MIN_BYTES:
            failures.append(f"Too short (<{MIN_BYTES} bytes): {relpath}")

    if failures:
        print("Full spectrum OS failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS: Dealix full-spectrum operating system exists.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
