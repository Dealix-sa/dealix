"""Dealix client acquisition queue package.

The package builds internal review queues and evidence-friendly records.
"""

from .models import ClientCard, QueueBundle, QueueItem
from .queue import build_queue, write_queue_bundle

__all__ = [
    "ClientCard",
    "QueueBundle",
    "QueueItem",
    "build_queue",
    "write_queue_bundle",
]
