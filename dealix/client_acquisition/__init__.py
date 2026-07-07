"""Dealix client acquisition queue package.

The package builds internal review queues and evidence-friendly records.
"""

from .models import ClientCard, QueueItem, QueueBundle
from .queue import build_queue, write_queue_bundle

__all__ = [
    "ClientCard",
    "QueueItem",
    "QueueBundle",
    "build_queue",
    "write_queue_bundle",
]
