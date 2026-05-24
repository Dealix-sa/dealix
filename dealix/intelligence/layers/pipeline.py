"""
Pipeline orchestrator — compose intelligence layers into named flows.
منسّق خطوط المعالجة — ربط طبقات الذكاء في تدفّقات قابلة للتسمية.

Lightweight, async-capable, with per-step timing + error capture. Each
step is a callable (sync or async) that takes the current context dict
and returns a dict to merge. Steps can short-circuit by setting
``context["__halt__"] = True``.
"""

from __future__ import annotations

import asyncio
import inspect
import time
import traceback
from dataclasses import dataclass, field
from typing import Any, Callable

StepFn = Callable[[dict[str, Any]], Any]


@dataclass
class PipelineStep:
    name: str
    fn: StepFn
    optional: bool = False
    timeout_s: float | None = None
    description: str = ""


@dataclass
class StepResult:
    name: str
    ok: bool
    duration_ms: float
    output_keys: tuple[str, ...]
    error: str = ""


@dataclass
class PipelineRun:
    name: str
    context: dict[str, Any] = field(default_factory=dict)
    steps: list[StepResult] = field(default_factory=list)
    halted: bool = False
    total_duration_ms: float = 0.0


class Pipeline:
    """Compose steps; run once per input."""

    def __init__(self, name: str) -> None:
        if not name:
            raise ValueError("pipeline name required")
        self.name = name
        self._steps: list[PipelineStep] = []

    # ── Build ─────────────────────────────────────────────────────
    def add(
        self,
        name: str,
        fn: StepFn,
        *,
        optional: bool = False,
        timeout_s: float | None = None,
        description: str = "",
    ) -> "Pipeline":
        if not name:
            raise ValueError("step name required")
        if not callable(fn):
            raise TypeError("step fn must be callable")
        self._steps.append(
            PipelineStep(
                name=name,
                fn=fn,
                optional=optional,
                timeout_s=timeout_s,
                description=description,
            )
        )
        return self

    def steps(self) -> list[dict[str, Any]]:
        return [
            {
                "name": s.name,
                "optional": s.optional,
                "timeout_s": s.timeout_s,
                "description": s.description,
            }
            for s in self._steps
        ]

    # ── Run ───────────────────────────────────────────────────────
    async def run(self, initial: dict[str, Any] | None = None) -> PipelineRun:
        run = PipelineRun(name=self.name, context=dict(initial or {}))
        start_total = time.perf_counter()
        for step in self._steps:
            if run.context.get("__halt__"):
                run.halted = True
                break
            start = time.perf_counter()
            try:
                coro = self._invoke(step, run.context)
                if step.timeout_s is not None:
                    output = await asyncio.wait_for(coro, timeout=step.timeout_s)
                else:
                    output = await coro
                duration = (time.perf_counter() - start) * 1000
                if output is None:
                    output = {}
                if not isinstance(output, dict):
                    raise TypeError(f"step '{step.name}' must return a dict (got {type(output).__name__})")
                run.context.update(output)
                run.steps.append(
                    StepResult(
                        name=step.name,
                        ok=True,
                        duration_ms=round(duration, 2),
                        output_keys=tuple(output.keys()),
                    )
                )
            except Exception as exc:  # noqa: BLE001
                duration = (time.perf_counter() - start) * 1000
                err = f"{type(exc).__name__}: {exc}"
                run.steps.append(
                    StepResult(
                        name=step.name,
                        ok=False,
                        duration_ms=round(duration, 2),
                        output_keys=tuple(),
                        error=err,
                    )
                )
                run.context.setdefault("__errors__", []).append(
                    {
                        "step": step.name,
                        "error": err,
                        "traceback": traceback.format_exc(limit=4),
                    }
                )
                if not step.optional:
                    run.halted = True
                    break
        run.total_duration_ms = round((time.perf_counter() - start_total) * 1000, 2)
        return run

    def run_sync(self, initial: dict[str, Any] | None = None) -> PipelineRun:
        return asyncio.get_event_loop().run_until_complete(self.run(initial))

    # ── Internals ─────────────────────────────────────────────────
    @staticmethod
    async def _invoke(step: PipelineStep, ctx: dict[str, Any]) -> Any:
        result = step.fn(ctx)
        if inspect.isawaitable(result):
            return await result  # type: ignore[return-value]
        return result
