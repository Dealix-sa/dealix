"""
TrustSignalBuilder — emit a JSON-LD block summarising the trust signals
for a given page subject. Used by AI answer engines as a verification
hook.
"""

from __future__ import annotations

from dealix.hermes.growth.trust_signals import TrustSignal, TrustSignalLedger


def build_trust_signal_block(subject: str, ledger: TrustSignalLedger) -> dict[str, object]:
    signals: list[TrustSignal] = ledger.for_subject(subject)
    return {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": f"{subject} — trust signals",
        "about": [
            {
                "@type": "CreativeWork",
                "name": s.kind.value,
                "identifier": s.signal_id,
                "url": s.url,
                "dateCreated": s.captured_at.isoformat(),
            }
            for s in signals
        ],
    }
