# PixelRAG Visual Evidence Layer for Dealix

## Executive decision

PixelRAG should be integrated into Dealix as an optional **Visual Evidence Layer**, not as a hard production dependency.

The reason is simple: Dealix currently supports Python 3.11+, while PixelRAG requires Python 3.12 and has heavy optional ML/indexing dependencies. A direct dependency would risk breaking Dealix CI, Railway production, and the existing commercial launch path.

Instead, Dealix should use PixelRAG through a safe adapter boundary:

```txt
Dealix Proof / Market / B2G workflows
        |
        v
VisualRAG adapter contract
        |
        +-- disabled/no-op mode for CI and production safety
        +-- hosted PixelRAG API mode for low-friction experiments
        +-- local PixelRAG service mode for private client documents
        +-- pixelshot CLI mode for screenshot capture only
```

## What PixelRAG gives Dealix

PixelRAG renders pages, PDFs, and documents as screenshots and retrieves over the visual tiles. This matters because many commercial documents are not text-first:

- PDFs with tables and charts.
- Competitor pricing pages with layout-sensitive sections.
- B2G and enterprise requirements documents.
- Client proof packs and screenshots.
- Investor decks and product brochures.
- Scanned or visually formatted reports.

Traditional text extraction often loses tables, charts, sidebars, and layout. PixelRAG keeps the visual surface and allows retrieval over the screenshot tiles.

## Highest-value Dealix use cases

### 1. Proof Pack visual evidence

Use PixelRAG to attach visual source tiles to claims inside Dealix proof packs:

- show the exact page/tile supporting a market claim;
- preserve screenshots from competitor pages;
- attach visual evidence for before/after revenue leaks;
- avoid fake proof by linking claims to rendered evidence.

### 2. B2G readiness document intelligence

For B2G and enterprise readiness, documents often contain tables, eligibility matrices, scope sections, and compliance requirements. PixelRAG can help retrieve the exact visual section rather than relying only on parsed text.

### 3. Saudi Market Access snapshots

For foreign companies entering Saudi Arabia, Dealix can generate a market access snapshot with visual evidence tiles from:

- public pages;
- PDFs;
- brochures;
- event exhibitor pages;
- competitor pages;
- sector reports.

### 4. Client document intake

When a client uploads PDFs, screenshots, or brochures, Dealix can render them to visual tiles and search them by semantic questions:

- "Where does the proposal mention pricing?"
- "Which page contains the partner responsibilities table?"
- "Where is the eligibility matrix?"
- "Which section shows the implementation timeline?"

### 5. Visual agent browsing

PixelRAG includes `pixelshot`, which can render a page to screenshot tiles. This gives Dealix agents a safer way to inspect page layout and visual evidence without over-trusting raw HTML extraction.

## Integration boundaries

### Do now

- Add Dealix adapter contracts.
- Add policy gates for client documents and screenshots.
- Add CLI/demo runner that works without PixelRAG installed.
- Add verification that proves the integration remains optional.
- Document deployment modes.

### Do later

- Run a separate Python 3.12 PixelRAG worker.
- Use GPU/on-demand workers for embedding-heavy indexing.
- Add vector index persistence for private client documents.
- Add admin UI to show visual evidence tiles in proof packs.

### Do not do now

- Do not vendor the PixelRAG repository into Dealix.
- Do not add `pixelrag` as a mandatory dependency in Dealix `pyproject.toml`.
- Do not run large FAISS/Wikipedia indexes inside the main Railway web service.
- Do not expose a local PixelRAG or Ollama endpoint publicly.
- Do not use visual retrieval to bypass site terms or access controls.

## Recommended architecture

```txt
Dealix main app, Python 3.11
  - proof pack generator
  - B2G readiness engine
  - market access snapshot generator
  - visual_rag adapter contract

PixelRAG worker, Python 3.12, separate runtime
  - pixelshot rendering
  - pixelrag index/build/serve
  - optional GPU/MPS/CPU embedding
  - private API endpoint

Storage
  - rendered visual tiles
  - source metadata
  - retrieval results
  - proof ledger links
```

## Deployment modes

### Mode 0: disabled

Default for CI and production until explicitly enabled. Dealix should return structured `disabled` results with clear next steps.

### Mode 1: screenshot-only

Use `pixelshot` to render pages or PDFs into tiles for human review and proof-pack evidence. This is the lowest-risk first practical benefit.

### Mode 2: external API search

Use a hosted PixelRAG-compatible search endpoint for non-sensitive public documents only.

### Mode 3: private worker

Run PixelRAG as a separate private worker for client documents. This is the correct mode for PDPL-sensitive or proprietary materials.

## Policy rules

Every visual evidence job must define:

- source URL or local document path;
- sensitivity class;
- permitted mode;
- retention policy;
- whether external processing is allowed;
- human approval requirement;
- proof-pack destination.

Sensitive client materials must use local/private worker mode only.

## Commercial impact

PixelRAG improves Dealix positioning in three ways:

1. **Trust** — Dealix can show visual evidence behind claims.
2. **B2G readiness** — tables and formatted PDF requirements become searchable.
3. **Differentiation** — Dealix becomes more than CRM/RAG; it becomes a proof-driven visual intelligence layer for Saudi market access.

## First production-safe milestone

The first milestone is not full indexing. It is:

```txt
Visual source -> screenshot tiles -> human-reviewed evidence -> proof pack link
```

This gives immediate client value without GPU cost, large indexes, or production risk.
