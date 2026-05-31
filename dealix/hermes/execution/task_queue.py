"""
Task Queue — قائمة بسيطة في الذاكرة. يُستبدل بـ Postgres-backed queue لاحقًا
بنفس الواجهة (يربط بجدول `hermes_workflow_runs`).
"""

from __future__ import annotations

import heapq
import itertools
import threading
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any, Protocol


class TaskStatus(StrEnum):
    QUEUED = "queued"
    LEASED = "leased"
    DONE = "done"
    FAILED = "failed"
    DEAD = "dead"


@dataclass(order=True)
class Task:
    priority: int
    enqueued_at: float = field(compare=True)
    task_id: str = field(compare=False, default_factory=lambda: f"tsk_{uuid.uuid4().hex[:14]}")
    kind: str = field(compare=False, default="generic")
    payload: dict[str, Any] = field(compare=False, default_factory=dict)
    attempts: int = field(compare=False, default=0)
    max_attempts: int = field(compare=False, default=3)
    status: TaskStatus = field(compare=False, default=TaskStatus.QUEUED)
    last_error: str | None = field(compare=False, default=None)


class TaskQueue(Protocol):
    def enqueue(self, task: Task) -> None: ...
    def lease(self) -> Task | None: ...
    def ack(self, task_id: str) -> None: ...
    def fail(self, task_id: str, reason: str) -> None: ...


class InMemoryTaskQueue:
    def __init__(self) -> None:
        self._heap: list[Task] = []
        self._by_id: dict[str, Task] = {}
        self._lock = threading.Lock()
        self._counter = itertools.count()

    def enqueue(self, task: Task) -> None:
        task.enqueued_at = datetime.now(timezone.utc).timestamp() + next(self._counter) * 1e-9
        with self._lock:
            heapq.heappush(self._heap, task)
            self._by_id[task.task_id] = task

    def lease(self) -> Task | None:
        with self._lock:
            while self._heap:
                task = heapq.heappop(self._heap)
                if task.status == TaskStatus.QUEUED:
                    task.status = TaskStatus.LEASED
                    task.attempts += 1
                    return task
            return None

    def ack(self, task_id: str) -> None:
        with self._lock:
            task = self._by_id.get(task_id)
            if task:
                task.status = TaskStatus.DONE

    def fail(self, task_id: str, reason: str) -> None:
        with self._lock:
            task = self._by_id.get(task_id)
            if not task:
                return
            task.last_error = reason
            if task.attempts >= task.max_attempts:
                task.status = TaskStatus.DEAD
            else:
                task.status = TaskStatus.QUEUED
                heapq.heappush(self._heap, task)


__all__ = ["InMemoryTaskQueue", "Task", "TaskQueue", "TaskStatus"]
