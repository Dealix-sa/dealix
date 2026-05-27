#!/usr/bin/env bash
# Deploy Dealix production stack with monitoring add-ons.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

ENV_FILE="${ENV_FILE:-.env.prod}"
if [[ ! -f "$ENV_FILE" ]]; then
  echo "Missing $ENV_FILE. Copy .env.prod.example to .env.prod and fill real values."
  exit 1
fi

export GIT_SHA="${GIT_SHA:-$(git rev-parse --short HEAD 2>/dev/null || echo local)}"
export IMAGE_TAG="${IMAGE_TAG:-$GIT_SHA}"

COMPOSE="docker compose --env-file $ENV_FILE -f docker-compose.prod.yml -f docker-compose.monitoring.yml"

$COMPOSE build
$COMPOSE up -d --remove-orphans
$COMPOSE ps

echo "DEALIX_MONITORING_DEPLOY_OK"
