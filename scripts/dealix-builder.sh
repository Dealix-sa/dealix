#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../dealix-builder-api"
node src/cli.js "$@"
