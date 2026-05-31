"""
Sandbox — تشغيل دالّة محدودة الزمن داخل thread.

لا يستخدم subprocess. الهدف عزل دالّة قابلة للفشل أو دالّة قد تتعلّق
زمنيًا، مع التقاط الاستثناءات وقياس الزمن المنقضي.
"""

from __future__ import annotations

import threading
import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass
class SandboxResult:
    ok: bool
    output: Any
    error: str | None
    elapsed_s: float


class Sandbox:
    """منفّذ دوال داخل thread مع timeout."""

    def run(
        self,
        fn: Callable[..., Any],
        args: dict[str, Any] | None = None,
        timeout_s: float = 5.0,
    ) -> SandboxResult:
        if not callable(fn):
            raise TypeError("fn must be callable")
        if args is None:
            args = {}
        if not isinstance(args, dict):
            raise TypeError("args must be dict[str, Any]")
        if timeout_s <= 0:
            raise ValueError("timeout_s must be positive")

        holder: dict[str, Any] = {"output": None, "error": None}

        def _target() -> None:
            try:
                holder["output"] = fn(**args)
            except Exception as exc:  # noqa: BLE001 — boundary
                holder["error"] = f"{type(exc).__name__}: {exc}"

        # daemon=True حتى لا يحجز إيقاف العملية.
        thread = threading.Thread(target=_target, daemon=True)
        start = time.monotonic()
        thread.start()
        thread.join(timeout=timeout_s)
        elapsed = time.monotonic() - start

        if thread.is_alive():
            # الـ thread ما زال يعمل — نُعلّمه كـ timeout. لا يمكن قتله بأمان
            # في cpython العادي؛ نتركه يكمل في الخلفية لكن النتيجة timeout.
            return SandboxResult(
                ok=False,
                output=None,
                error=f"timeout_after_{timeout_s:.3f}s",
                elapsed_s=elapsed,
            )

        if holder["error"] is not None:
            return SandboxResult(
                ok=False,
                output=None,
                error=holder["error"],
                elapsed_s=elapsed,
            )

        return SandboxResult(
            ok=True,
            output=holder["output"],
            error=None,
            elapsed_s=elapsed,
        )


__all__ = ["Sandbox", "SandboxResult"]
