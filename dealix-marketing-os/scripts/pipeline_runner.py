"""Pipeline runner: master orchestrator for the full draft factory pipeline."""

from __future__ import annotations

import argparse
import logging
import sys
import time
from pathlib import Path
from typing import Callable

BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from dotenv import load_dotenv

load_dotenv(BASE_DIR.parent / ".env")

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger(__name__)


def run_market_scanner(dry_run: bool, company_limit: int) -> bool:
    if dry_run:
        log.info("[DRY RUN] Would run market_scanner --count %d", company_limit)
        return True
    try:
        from dealix_marketing_os.scripts import market_scanner
        market_scanner.run(sector_id=None, count=company_limit)
        return True
    except Exception:
        pass
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "market_scanner",
            BASE_DIR / "scripts" / "market_scanner.py",
        )
        mod = importlib.util.loader_from_spec(spec)  # type: ignore
        spec.loader.exec_module(mod)  # type: ignore
        mod.run(None, company_limit)
        return True
    except Exception as exc:
        log.error("market_scanner failed: %s", exc)
        return False


def run_company_researcher(dry_run: bool, company_limit: int) -> bool:
    if dry_run:
        log.info("[DRY RUN] Would run company_researcher --limit %d", company_limit)
        return True
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "company_researcher",
            BASE_DIR / "scripts" / "company_researcher.py",
        )
        mod = importlib.util.util.load_module_from_spec(spec)  # type: ignore
        spec.loader.exec_module(mod)  # type: ignore
        mod.run(company_limit)
        return True
    except Exception as exc:
        log.error("company_researcher failed: %s", exc)
        return False


def run_offer_router(dry_run: bool, company_limit: int) -> bool:
    if dry_run:
        log.info("[DRY RUN] Would run offer_router")
        return True
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "offer_router",
            BASE_DIR / "scripts" / "offer_router.py",
        )
        mod = importlib.util.util.load_module_from_spec(spec)  # type: ignore
        spec.loader.exec_module(mod)  # type: ignore
        mod.run()
        return True
    except Exception as exc:
        log.error("offer_router failed: %s", exc)
        return False


def run_draft_writer(dry_run: bool, company_limit: int) -> bool:
    if dry_run:
        log.info("[DRY RUN] Would run draft_writer")
        return True
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "draft_writer",
            BASE_DIR / "scripts" / "draft_writer.py",
        )
        mod = importlib.util.util.load_module_from_spec(spec)  # type: ignore
        spec.loader.exec_module(mod)  # type: ignore
        mod.run()
        return True
    except Exception as exc:
        log.error("draft_writer failed: %s", exc)
        return False


def run_quality_gate(dry_run: bool, company_limit: int) -> bool:
    if dry_run:
        log.info("[DRY RUN] Would run draft_quality_gate")
        return True
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "draft_quality_gate",
            BASE_DIR / "scripts" / "draft_quality_gate.py",
        )
        mod = importlib.util.util.load_module_from_spec(spec)  # type: ignore
        spec.loader.exec_module(mod)  # type: ignore
        mod.run()
        return True
    except Exception as exc:
        log.error("draft_quality_gate failed: %s", exc)
        return False


def run_founder_report(dry_run: bool, company_limit: int) -> bool:
    if dry_run:
        log.info("[DRY RUN] Would run founder_marketing_report")
        return True
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "founder_marketing_report",
            BASE_DIR / "scripts" / "founder_marketing_report.py",
        )
        mod = importlib.util.util.load_module_from_spec(spec)  # type: ignore
        spec.loader.exec_module(mod)  # type: ignore
        mod.run()
        return True
    except Exception as exc:
        log.error("founder_marketing_report failed: %s", exc)
        return False


def _load_step_fn(script_name: str, fn_name: str = "run") -> Callable | None:
    import importlib.util
    path = BASE_DIR / "scripts" / f"{script_name}.py"
    try:
        spec = importlib.util.spec_from_file_location(script_name, path)
        if spec is None or spec.loader is None:
            return None
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)  # type: ignore
        return getattr(mod, fn_name, None)
    except Exception as exc:
        log.error("Failed to load %s: %s", script_name, exc)
        return None


PIPELINE_STEPS = [
    ("scan", "market_scanner"),
    ("research", "company_researcher"),
    ("route", "offer_router"),
    ("draft", "draft_writer"),
    ("gate", "draft_quality_gate"),
    ("report", "founder_marketing_report"),
]

STEP_ARGS: dict[str, list] = {
    "scan": ["sector_id", "count"],
    "research": ["limit"],
    "route": [],
    "draft": [],
    "gate": [],
    "report": [],
}


def run(steps: list[str], dry_run: bool, company_limit: int) -> None:
    print(f"\nDealix Pipeline Runner")
    print(f"Steps: {', '.join(steps)}")
    print(f"Company limit: {company_limit}")
    print(f"Dry run: {dry_run}\n")

    results: list[dict] = []
    total_start = time.time()

    for step_id, script_name in PIPELINE_STEPS:
        if step_id not in steps:
            log.info("Skipping step: %s", step_id)
            continue

        print(f"--- Step: {step_id} ---")
        step_start = time.time()

        if dry_run:
            log.info("[DRY RUN] %s", script_name)
            elapsed = time.time() - step_start
            results.append({"step": step_id, "status": "dry_run", "elapsed_s": round(elapsed, 2)})
            continue

        fn = _load_step_fn(script_name)
        if fn is None:
            log.error("Could not load %s", script_name)
            results.append({"step": step_id, "status": "load_failed", "elapsed_s": 0})
            continue

        try:
            step_args_keys = STEP_ARGS.get(step_id, [])
            if step_id == "scan":
                fn(sector_id=None, count=company_limit)
            elif step_id == "research":
                fn(limit=company_limit)
            else:
                fn()
            elapsed = time.time() - step_start
            results.append({"step": step_id, "status": "ok", "elapsed_s": round(elapsed, 2)})
            log.info("Step %s completed in %.1fs", step_id, elapsed)
        except Exception as exc:
            elapsed = time.time() - step_start
            log.error("Step %s failed: %s", step_id, exc)
            results.append({"step": step_id, "status": "failed", "error": str(exc), "elapsed_s": round(elapsed, 2)})

    total_elapsed = time.time() - total_start
    print(f"\nPipeline complete in {total_elapsed:.1f}s")
    for r in results:
        status_str = r["status"].upper()
        print(f"  {r['step']:10s} {status_str:12s} {r['elapsed_s']:.1f}s")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Dealix draft factory pipeline")
    parser.add_argument(
        "--steps",
        default="scan,research,route,draft,gate,report",
        help="Comma-separated steps to run",
    )
    parser.add_argument("--dry-run", action="store_true", help="Simulate without API calls")
    parser.add_argument("--company-limit", type=int, default=20, help="Max companies to process")
    args = parser.parse_args()

    steps = [s.strip() for s in args.steps.split(",") if s.strip()]
    valid_step_ids = {s[0] for s in PIPELINE_STEPS}
    invalid = [s for s in steps if s not in valid_step_ids]
    if invalid:
        log.error("Unknown steps: %s. Valid: %s", invalid, sorted(valid_step_ids))
        sys.exit(1)

    run(steps, args.dry_run, args.company_limit)


if __name__ == "__main__":
    main()
