"""Draft quality gate: evaluates and scores generated drafts via Claude."""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from datetime import date, datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from dotenv import load_dotenv

load_dotenv(BASE_DIR.parent / ".env")

import yaml

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)

MEMORY_DIR = BASE_DIR / "memory"
CONFIG_DIR = BASE_DIR / "config"
OUTPUTS_DIR = BASE_DIR / "outputs"
DRAFT_QUEUE_PATH = MEMORY_DIR / "draft_queue.jsonl"


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    records = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return records


def rewrite_jsonl(path: Path, records: list[dict]) -> None:
    with open(path, "w") as fh:
        for rec in records:
            fh.write(json.dumps(rec) + "\n")


def load_persuasion_config() -> dict:
    with open(CONFIG_DIR / "persuasion.yml") as fh:
        return yaml.safe_load(fh)


def evaluate_draft_via_claude(draft: dict, persuasion_config: dict) -> dict | None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        log.error("ANTHROPIC_API_KEY not set")
        return None

    import anthropic

    client = anthropic.Anthropic(api_key=api_key)

    dimensions = persuasion_config.get("quality_gate", {}).get("dimensions", [])
    dim_text = "\n".join(
        f"- {d['id']} (max {d['max_score']}): {d['description']}"
        for d in dimensions
    )

    draft_content = f"Subject: {draft.get('subject', '')}\n\n{draft.get('body', '')}"

    prompt = f"""You are a B2B outreach quality evaluator. Score this draft against the rubric.

Company: {draft.get('company_name', '')}
Draft type: {draft.get('draft_type', '')}

Draft content:
---
{draft_content}
---

Scoring rubric:
{dim_text}

Evaluate each dimension strictly. Return a JSON object with:
{{
  "scores": {{
    "personalization": 0,
    "relevance": 0,
    "clarity": 0,
    "commercial_value": 0,
    "credibility": 0,
    "compliance": 0
  }},
  "total_score": 0,
  "issues": ["list of specific issues found"],
  "improvement_notes": "specific instructions to improve this draft"
}}

COMPLIANCE score must be 0 if the draft contains:
- Guaranteed outcome language ("guarantee", "assured", "100% ROI")
- Cold WhatsApp references
- LinkedIn automation references
- Scraping references

Return only valid JSON. No explanation."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = message.content[0].text.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return json.loads(raw)
    except Exception as exc:
        log.error("Quality evaluation failed for draft %s: %s", draft.get("id"), exc)
        return None


def improve_draft_via_claude(draft: dict, evaluation: dict, persuasion_config: dict) -> dict | None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return None

    import anthropic

    client = anthropic.Anthropic(api_key=api_key)

    auto_improve = persuasion_config.get("auto_improve", {})
    instruction = auto_improve.get("instruction", "Rewrite applying the SPECIFIC-PAIN-PROOF-ASK formula.")

    draft_content = f"Subject: {draft.get('subject', '')}\n\n{draft.get('body', '')}"

    prompt = f"""You are a B2B outreach specialist. Improve this underperforming draft.

Company: {draft.get('company_name', '')}
Draft type: {draft.get('draft_type', '')}

Original draft:
---
{draft_content}
---

Issues identified:
{json.dumps(evaluation.get('issues', []), indent=2)}

Improvement notes:
{evaluation.get('improvement_notes', '')}

Improvement instruction:
{instruction}

Return a JSON object with:
{{
  "subject": "improved subject line (empty for non-email)",
  "body": "improved body content"
}}

Return only valid JSON. No explanation."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = message.content[0].text.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return json.loads(raw)
    except Exception as exc:
        log.error("Draft improvement failed for %s: %s", draft.get("id"), exc)
        return None


def run() -> None:
    persuasion_config = load_persuasion_config()
    min_score = persuasion_config.get("quality_gate", {}).get("minimum_score", 82)

    drafts = read_jsonl(DRAFT_QUEUE_PATH)
    eligible = [d for d in drafts if d.get("status") == "draft_generated"]

    if not eligible:
        log.info("No drafts to evaluate")
        return

    draft_map = {d["id"]: d for d in drafts}
    approved = 0
    rejected_list = []
    improved = 0

    for draft in eligible:
        log.info("Evaluating draft %s (%s)", draft.get("id"), draft.get("draft_type"))
        evaluation = evaluate_draft_via_claude(draft, persuasion_config)
        if not evaluation:
            continue

        total = evaluation.get("total_score", 0)
        issues = evaluation.get("issues", [])

        if total >= min_score:
            draft_map[draft["id"]].update({
                "quality_score": total,
                "approved_for_review": True,
                "approved_for_founder_review": True,
                "issues": issues,
                "score_breakdown": evaluation.get("scores", {}),
                "status": "approved_for_review",
                "evaluated_at": datetime.utcnow().isoformat() + "Z",
            })
            approved += 1
            log.info("APPROVED: %s score=%d", draft.get("id"), total)
        else:
            log.info("BELOW THRESHOLD: %s score=%d — attempting improvement", draft.get("id"), total)
            improved_content = improve_draft_via_claude(draft, evaluation, persuasion_config)

            if improved_content:
                draft_map[draft["id"]]["subject"] = improved_content.get("subject", draft.get("subject", ""))
                draft_map[draft["id"]]["body"] = improved_content.get("body", draft.get("body", ""))

                re_eval = evaluate_draft_via_claude(draft_map[draft["id"]], persuasion_config)
                if re_eval:
                    new_total = re_eval.get("total_score", 0)
                    if new_total >= min_score:
                        draft_map[draft["id"]].update({
                            "quality_score": new_total,
                            "approved_for_review": True,
                            "approved_for_founder_review": True,
                            "issues": re_eval.get("issues", []),
                            "score_breakdown": re_eval.get("scores", {}),
                            "status": "approved_for_review",
                            "auto_improved": True,
                            "evaluated_at": datetime.utcnow().isoformat() + "Z",
                        })
                        improved += 1
                        approved += 1
                        log.info("IMPROVED+APPROVED: %s new_score=%d", draft.get("id"), new_total)
                        continue
                    else:
                        draft_map[draft["id"]].update({
                            "quality_score": new_total,
                            "approved_for_review": False,
                            "issues": re_eval.get("issues", []),
                            "score_breakdown": re_eval.get("scores", {}),
                        })

            draft_map[draft["id"]].update({
                "approved_for_review": False,
                "approved_for_founder_review": False,
                "status": "rejected",
                "evaluated_at": datetime.utcnow().isoformat() + "Z",
            })
            rejected_list.append(draft_map[draft["id"]])
            log.info("REJECTED: %s score=%d", draft.get("id"), draft_map[draft["id"]].get("quality_score", 0))

    rewrite_jsonl(DRAFT_QUEUE_PATH, list(draft_map.values()))

    if rejected_list:
        rejected_dir = OUTPUTS_DIR / "rejected"
        rejected_dir.mkdir(parents=True, exist_ok=True)
        rejected_path = rejected_dir / f"{date.today().isoformat()}_rejected.jsonl"
        with open(rejected_path, "a") as fh:
            for rec in rejected_list:
                fh.write(json.dumps(rec) + "\n")
        log.info("Wrote %d rejected drafts to %s", len(rejected_list), rejected_path)

    total_evaluated = len(eligible)
    total_rejected = len(rejected_list)
    print(
        f"Evaluated {total_evaluated} drafts: {approved} approved, {total_rejected} rejected, {improved} improved"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate draft quality and gate low-scoring drafts")
    parser.parse_args()
    run()


if __name__ == "__main__":
    main()
