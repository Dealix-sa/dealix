# Open Design Import Decision

## Decision

Do not import the full `nexu-io/open-design` repository into Dealix.

## Reason

Open Design is a standalone local-first desktop/design workspace with its own runtime assumptions, toolchain, package layout, media assets, and product direction. Dealix should adopt the operating model, not vendor the product.

## Adopted concepts

- Design systems as brand contracts
- Skills as repeatable artifact generators
- Artifact lifecycle and approval states
- Multi-agent compatibility
- Sandboxed/review-first mindset
- Clear agent repository guidance

## Rejected imports

- full source tree
- Electron runtime
- Open Design package manager constraints
- media assets
- plugin store
- desktop release architecture
- daemon runtime

## Dealix target

A Dealix-native Design Command Room OS integrated with Dealix's existing command room, revenue, delivery, proof pack, and trust/safety surfaces.
