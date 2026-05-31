"""Asset library facade — wraps the kernel's AssetStore."""

from __future__ import annotations

from dealix.hermes.kernel.assets import AssetStore


class AssetLibrary(AssetStore):
    """Currently identical to AssetStore — kept for callers that prefer the domain name."""
