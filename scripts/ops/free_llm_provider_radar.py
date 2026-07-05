#!/usr/bin/env python3
"""Dealix Free LLM Provider Radar.

Offline, dependency-free helper that reads the curated provider registry and
prints the best non-confidential providers for the requested operating task.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = ROOT / "data" / "ai" / "free_llm_provider_registry.json"

TASK_TAGS = {
    "coding": {"coding", "fast_coding", "github_native_prototyping", "agent_fallback"},
    "arabic": {"arabic_drafts", "translation", "customer_language_variants", "content"},
    "batch": {"batch_drafts", "bulk_drafts", "daily_operator", "lightweight_batch", "draft_generation"},
    "transcription": {"transcription"},
    "edge": {"edge_ai", "worker_experiments", "web_app_ai_gateway"},
    "sensitive": set(),
}

SENSITIVE_NOTICE = (
    "Sensitive/customer/legal/production data must stay on approved paid, "
    "private, or local providers. Free tiers are only for non-confidential "
    "drafts, coding help, and experiments."
)


def load_registry(path: Path = REGISTRY_PATH) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"Registry not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def provider_score(provider: dict[str, Any], task: str) -> int:
    if task == "sensitive":
        return 0
    uses = set(provider.get("dealix_uses", []))
    tags = TASK_TAGS.get(task, set())
    score = len(uses & tags) * 10
    if provider.get("openai_compatible"):
        score += 3
    if provider.get("free_or_trial") == "free":
        score += 2
    return score


def ranked_providers(registry: dict[str, Any], task: str, limit: int) -> list[dict[str, Any]]:
    providers = registry.get("providers", [])
    ranked = sorted(
        providers,
        key=lambda item: (provider_score(item, task), item.get("name", "")),
        reverse=True,
    )
    if task == "sensitive":
        return []
    return [item for item in ranked if provider_score(item, task) > 0][:limit]


def render_markdown(registry: dict[str, Any], task: str, limit: int) -> str:
    lines = [
        "# Dealix AI Provider Radar",
        "",
        f"Task: `{task}`",
        f"Registry reviewed: `{registry.get('last_reviewed', 'unknown')}`",
        f"Adopted from: {registry.get('adopted_from', 'unknown')}",
        "",
        f"> Safety: {SENSITIVE_NOTICE}",
        "",
    ]

    if task == "sensitive":
        lines.extend(
            [
                "## Recommendation",
                "",
                "Do not use free providers for this task. Use approved paid/private/local models, keep audit logs, and require human approval.",
                "",
            ]
        )
        return "\n".join(lines)

    providers = ranked_providers(registry, task, limit)
    lines.extend(["## Recommended providers", ""])
    for index, provider in enumerate(providers, start=1):
        models = ", ".join(provider.get("recommended_models", [])[:4]) or "review provider dashboard"
        uses = ", ".join(provider.get("dealix_uses", []))
        lines.extend(
            [
                f"### {index}. {provider['name']}",
                "",
                f"- Base URL: `{provider.get('base_url', 'n/a')}`",
                f"- OpenAI-compatible: `{provider.get('openai_compatible')}`",
                f"- Tier: `{provider.get('free_or_trial', 'unknown')}`",
                f"- Limits: {provider.get('limits_summary', 'review current provider docs')}",
                f"- Models: {models}",
                f"- Dealix uses: {uses}",
                f"- Private data: `{provider.get('private_data', 'do_not_send')}`",
                "",
            ]
        )

    lines.extend(
        [
            "## Operator action",
            "",
            "1. Pick the first provider that has an active key in `.env` or your secret manager.",
            "2. Keep prompts non-confidential unless provider policy is approved.",
            "3. Generate drafts only; do not send external messages without Dealix approval gates.",
            "4. If limits are hit, move to the next provider in this radar.",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Print Dealix daily free LLM provider radar.")
    parser.add_argument(
        "--task",
        choices=sorted(TASK_TAGS.keys()),
        default="coding",
        help="Operating task to optimize for.",
    )
    parser.add_argument("--limit", type=int, default=5, help="Maximum provider recommendations.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args()

    registry = load_registry()
    providers = ranked_providers(registry, args.task, args.limit)

    if args.json:
        payload = {
            "task": args.task,
            "safety_notice": SENSITIVE_NOTICE,
            "last_reviewed": registry.get("last_reviewed"),
            "adopted_from": registry.get("adopted_from"),
            "providers": providers,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    print(render_markdown(registry, args.task, args.limit))


if __name__ == "__main__":
    main()
