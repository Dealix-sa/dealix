"""
Source Verifier — تحقّق من سلامة روابط المصادر.

شروط القبول:
    - https فقط (لا http، لا ftp، لا file، لا javascript).
    - لا localhost / 127.0.0.1.
    - لا IPv4 literal.
    - لا روابط مختصرة (bit.ly، t.co، goo.gl، ...).
    - host لا يحتوي على credentials (user:pass@).
"""

from __future__ import annotations

import ipaddress
from dataclasses import dataclass, field
from urllib.parse import urlparse


@dataclass
class SourceResult:
    url: str
    allowed: bool
    reasons: list[str] = field(default_factory=list)


_BLOCKED_HOSTS_EXACT: frozenset[str] = frozenset(
    {"localhost", "localhost.localdomain", "ip6-localhost"}
)

_SHORTENER_HOSTS: frozenset[str] = frozenset(
    {
        "bit.ly",
        "tinyurl.com",
        "t.co",
        "goo.gl",
        "ow.ly",
        "buff.ly",
        "is.gd",
        "rb.gy",
        "rebrand.ly",
        "cutt.ly",
        "shorturl.at",
        "lnkd.in",
        "fb.me",
        "youtu.be",
    }
)


def _is_ip_literal(host: str) -> bool:
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False


def _normalize_host(host: str | None) -> str:
    return (host or "").lower().strip()


class SourceVerifier:
    """يفحص قائمة روابط ويُرجع تقريرًا لكل رابط."""

    def verify(self, urls: list[str]) -> list[SourceResult]:
        if not isinstance(urls, list):
            raise TypeError("urls must be list[str]")

        results: list[SourceResult] = []
        for raw in urls:
            results.append(self._verify_one(raw))
        return results

    def _verify_one(self, raw: str) -> SourceResult:
        if not isinstance(raw, str) or not raw.strip():
            return SourceResult(
                url=raw if isinstance(raw, str) else "",
                allowed=False,
                reasons=["empty_or_invalid_url"],
            )

        try:
            parsed = urlparse(raw.strip())
        except Exception as exc:  # noqa: BLE001
            return SourceResult(url=raw, allowed=False, reasons=[f"parse_error:{exc!r}"])

        reasons: list[str] = []
        scheme = (parsed.scheme or "").lower()
        if scheme != "https":
            reasons.append(f"scheme_not_https:{scheme or 'missing'}")

        if parsed.username or parsed.password:
            reasons.append("embedded_credentials_in_url")

        host = _normalize_host(parsed.hostname)
        if not host:
            reasons.append("missing_host")
        else:
            if host in _BLOCKED_HOSTS_EXACT:
                reasons.append(f"blocked_host:{host}")

            if _is_ip_literal(host):
                reasons.append(f"ip_literal_disallowed:{host}")

            if host in _SHORTENER_HOSTS or any(
                host.endswith("." + sh) for sh in _SHORTENER_HOSTS
            ):
                reasons.append(f"link_shortener_disallowed:{host}")

        allowed = not reasons
        if allowed:
            reasons = ["ok"]
        return SourceResult(url=raw, allowed=allowed, reasons=reasons)


__all__ = ["SourceResult", "SourceVerifier"]
