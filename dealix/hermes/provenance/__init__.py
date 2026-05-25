"""
Provenance ledger.

Every prompt fragment, agent message, and tool output that flows through
Hermes is wrapped in a ProvenanceObject. The ledger records:

- where the data came from (source)
- how trusted that source is (trust level)
- which agent produced it
- which agents consumed it (lineage)
- whether it was sanitized before downstream use

Downstream validators MUST refuse to treat data from `untrusted` sources
as instructions.
"""

from __future__ import annotations

from dealix.hermes.provenance.downstream_validation import (
    DownstreamValidation,
    validate_for_downstream,
)
from dealix.hermes.provenance.ledger import ProvenanceLedger, ProvenanceObject
from dealix.hermes.provenance.output_lineage import (
    LineageGraph,
    build_lineage,
)
from dealix.hermes.provenance.source_metadata import (
    SourceMetadata,
    build_source_metadata,
)
from dealix.hermes.provenance.trust_level import TrustLevel, score_trust_level

__all__ = [
    "ProvenanceLedger",
    "ProvenanceObject",
    "SourceMetadata",
    "build_source_metadata",
    "TrustLevel",
    "score_trust_level",
    "LineageGraph",
    "build_lineage",
    "DownstreamValidation",
    "validate_for_downstream",
]
