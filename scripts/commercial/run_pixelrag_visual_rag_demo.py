#!/usr/bin/env python3
"""Run a small VisualRAG demonstration job for Dealix.

By default this script stays in safe pending-approval mode and does not call any
external service. Use it to show how a Dealix proof-pack workflow would prepare a
PixelRAG visual evidence job.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from dealix.visual_rag import (
    VisualRAGAdapter,
    VisualRAGJob,
    VisualRAGMode,
    VisualRAGSource,
    VisualRAGSensitivity,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a Dealix VisualRAG demo job")
    parser.add_argument("--job-id", default="demo-visual-rag")
    parser.add_argument("--source", default="https://example.com")
    parser.add_argument("--query", default="Find visual evidence for the main commercial claim")
    parser.add_argument(
        "--mode",
        choices=[mode.value for mode in VisualRAGMode],
        default=VisualRAGMode.DISABLED.value,
    )
    parser.add_argument(
        "--sensitivity",
        choices=[value.value for value in VisualRAGSensitivity],
        default=VisualRAGSensitivity.PUBLIC.value,
    )
    parser.add_argument("--approve", action="store_true", help="Execute instead of pending approval")
    parser.add_argument(
        "--allow-external-processing",
        action="store_true",
        help="Allow hosted processing for public sources only",
    )
    parser.add_argument("--output", default="reports/visual_rag/demo_result.json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    job = VisualRAGJob(
        job_id=args.job_id,
        mode=VisualRAGMode(args.mode),
        sources=[VisualRAGSource(kind="url", uri=args.source, title="Demo source")],
        query=args.query,
        sensitivity=VisualRAGSensitivity(args.sensitivity),
        allow_external_processing=args.allow_external_processing,
        require_human_approval=not args.approve,
        proof_pack_id="demo-proof-pack",
        metadata={"purpose": "Dealix PixelRAG integration demo"},
    )
    result = VisualRAGAdapter().run(job)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(result.model_dump_json(indent=2), encoding="utf-8")

    print(json.dumps(result.model_dump(mode="json"), indent=2, ensure_ascii=False))
    print(f"Wrote {output}")
    return 0 if result.status in {"disabled", "blocked", "pending_approval", "ok"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
