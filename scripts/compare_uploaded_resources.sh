#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# compare_uploaded_resources.sh
#
# Extracts uploaded Dealix OS / PR / roadmap resource archives into a temp
# workdir, summarizes their contents, computes checksums, and classifies each
# as a source candidate, build artifact, or resource/unknown.
#
# It NEVER writes into the repository source tree. It is a read-only review aid
# for the Extract -> Diff -> Select -> Branch -> PR -> CI -> Merge flow described
# in docs/ops/UPLOADED_RESOURCE_INTEGRATION_DECISION.md.
#
# Usage:
#   ./scripts/compare_uploaded_resources.sh [WORKDIR]
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail
shopt -s nullglob

ROOT="$(git rev-parse --show-toplevel)"
ARCHIVE_DIR="$ROOT/resources/company_os/uploaded_archives"
WORKDIR="${1:-/tmp/dealix_uploaded_compare}"

archives=("$ARCHIVE_DIR"/*.zip)
if [ ${#archives[@]} -eq 0 ]; then
  echo "No archives found in: $ARCHIVE_DIR"
  echo "Drop the uploaded *.zip files there, record them in"
  echo "resources/company_os/UPLOADED_ARCHIVES_MANIFEST.json, then re-run."
  exit 0
fi

rm -rf "$WORKDIR"
mkdir -p "$WORKDIR"

echo "== Checksums (record these in UPLOADED_ARCHIVES_MANIFEST.json) =="
for z in "${archives[@]}"; do
  if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$z"
  else
    shasum -a 256 "$z"
  fi
done
echo ""

echo "== Extracting uploaded resource archives =="
for z in "${archives[@]}"; do
  name="$(basename "$z" .zip)"
  mkdir -p "$WORKDIR/$name"
  unzip -q "$z" -d "$WORKDIR/$name"
  echo "Extracted: $name"
done
echo ""

echo "== Archive summaries (first 200 entries) =="
find "$WORKDIR" -maxdepth 3 -type f | sed "s#$WORKDIR/##" | sort | head -200
echo ""

echo "== Classification =="
for d in "$WORKDIR"/*/; do
  d="${d%/}"
  base="$(basename "$d")"
  if [ -d "$d/app/src" ] || [ -d "$d/src" ] || find "$d" -maxdepth 3 -name "*.tsx" -o -name "*.py" 2>/dev/null | grep -q .; then
    if find "$d" -maxdepth 3 -type d -name assets | grep -q . && ! find "$d" -maxdepth 4 -name "*.tsx" | grep -q .; then
      echo "BUILD_ARTIFACT_ONLY: $base"
    else
      echo "SOURCE_CANDIDATE:    $base"
    fi
  elif find "$d" -maxdepth 3 -type d -name assets | grep -q .; then
    echo "BUILD_ARTIFACT_ONLY: $base"
  else
    echo "RESOURCE_OR_UNKNOWN: $base"
  fi
done
echo ""

echo "== Diff hints (against this repo) =="
echo "  diff -ruN apps/web <archive>/app/src   | less"
echo "  diff -ruN os       <archive>/app/tests/os | less"
echo "  rsync --dry-run -av <archive>/app/ apps/web/"
echo ""
echo "Promote ONLY selected files, single-scope PRs, in the order from"
echo "docs/ops/UPLOADED_RESOURCE_INTEGRATION_DECISION.md."
