"""Rate limiting for outbound channels."""

from __future__ import annotations

import time
from collections import deque
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta

from app.outbound.config import OutboundSettings
from app.outbound.models import Channel


@dataclass
class ChannelBucket:
    """Token-bucket style window for one channel."""

    daily_limit: int
    batch_limit: int
    min_seconds_between_sends: int
    sent_today: deque[datetime] = field(default_factory=lambda: deque())
    last_sent_at: float = 0.0

    def prune(self, now: datetime) -> None:
        cutoff = now - timedelta(days=1)
        while self.sent_today and self.sent_today[0] < cutoff:
            self.sent_today.popleft()

    def can_send(self, now: datetime) -> tuple[bool, str]:
        self.prune(now)
        if len(self.sent_today) >= self.daily_limit:
            return False, f"Daily limit reached ({self.daily_limit})"
        elapsed = time.monotonic() - self.last_sent_at
        if self.last_sent_at and elapsed < self.min_seconds_between_sends:
            return (
                False,
                f"Rate limit: wait {self.min_seconds_between_sends - int(elapsed)}s",
            )
        return True, ""

    def record_send(self, now: datetime) -> None:
        self.sent_today.append(now)
        self.last_sent_at = time.monotonic()


class RateLimiter:
    """Tracks and enforces per-channel daily and inter-send limits."""

    def __init__(self, settings: OutboundSettings | None = None) -> None:
        self.settings = settings or OutboundSettings()
        self._buckets: dict[Channel, ChannelBucket] = {
            Channel.EMAIL: ChannelBucket(
                daily_limit=self.settings.email_daily_limit,
                batch_limit=self.settings.email_batch_limit,
                min_seconds_between_sends=self.settings.email_min_seconds_between_sends,
            ),
            Channel.WHATSAPP: ChannelBucket(
                daily_limit=self.settings.whatsapp_daily_limit,
                batch_limit=self.settings.whatsapp_batch_limit,
                min_seconds_between_sends=self.settings.whatsapp_min_seconds_between_sends,
            ),
        }

    def can_send(self, channel: Channel, now: datetime | None = None) -> tuple[bool, str]:
        now = now or datetime.now(UTC)
        return self._buckets[channel].can_send(now)

    def record_send(self, channel: Channel, now: datetime | None = None) -> None:
        now = now or datetime.now(UTC)
        self._buckets[channel].record_send(now)

    def remaining_today(self, channel: Channel) -> int:
        bucket = self._buckets[channel]
        bucket.prune(datetime.now(UTC))
        return max(0, bucket.daily_limit - len(bucket.sent_today))

    def check_batch(
        self, channel: Channel, count: int, now: datetime | None = None
    ) -> tuple[bool, str]:
        """Check whether a batch of `count` messages is within limits."""
        now = now or datetime.now(UTC)
        bucket = self._buckets[channel]
        bucket.prune(now)
        if count > bucket.batch_limit:
            return False, f"Batch size {count} exceeds limit {bucket.batch_limit}"
        if len(bucket.sent_today) + count > bucket.daily_limit:
            return False, f"Batch would exceed daily limit ({bucket.daily_limit})"
        return True, ""

    def summary(self) -> dict:
        return {
            "email": {
                "daily_limit": self._buckets[Channel.EMAIL].daily_limit,
                "remaining_today": self.remaining_today(Channel.EMAIL),
            },
            "whatsapp": {
                "daily_limit": self._buckets[Channel.WHATSAPP].daily_limit,
                "remaining_today": self.remaining_today(Channel.WHATSAPP),
            },
        }
