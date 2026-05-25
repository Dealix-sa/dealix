"""Trace a message origin chain and detect untrusted upstream hops."""

from __future__ import annotations

from dataclasses import dataclass, field

from .source_trust import trust_of


@dataclass(frozen=True)
class ProvenanceHop:
    source: str
    actor: str


@dataclass(frozen=True)
class ProvenanceReport:
    chain: tuple[ProvenanceHop, ...]
    min_trust_score: int
    weakest_hop: ProvenanceHop | None
    trustworthy: bool
    reasons: list[str] = field(default_factory=list)


def check(chain: list[ProvenanceHop], *, minimum: int = 50) -> ProvenanceReport:
    """Walk the provenance chain and report whether every hop meets the trust minimum."""
    reasons: list[str] = []
    if not chain:
        return ProvenanceReport(chain=(), min_trust_score=0, weakest_hop=None, trustworthy=False, reasons=["empty chain"])

    weakest: ProvenanceHop | None = None
    weakest_score = 101
    for hop in chain:
        s = trust_of(hop.source).score
        if s < weakest_score:
            weakest_score = s
            weakest = hop
        if s < minimum:
            reasons.append(f"hop {hop.actor} source={hop.source} score={s} < {minimum}")
    return ProvenanceReport(
        chain=tuple(chain),
        min_trust_score=weakest_score,
        weakest_hop=weakest,
        trustworthy=not reasons,
        reasons=reasons,
    )
