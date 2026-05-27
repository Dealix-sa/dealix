#!/usr/bin/env bash
# Install Hermes Agent OS hourly timer on the self-hosted server.
set -euo pipefail

if [[ "${EUID}" -ne 0 ]]; then
  echo "Run as root: sudo bash scripts/install_hermes_systemd.sh"
  exit 1
fi

ROOT="${DEALIX_ROOT:-/srv/dealix}"
DEPLOY_USER="${DEPLOY_USER:-dealix}"

if [[ ! -d "$ROOT" ]]; then
  echo "Missing $ROOT"
  exit 1
fi

install -m 0644 "$ROOT/ops/systemd/dealix-hermes.service" /etc/systemd/system/dealix-hermes.service
install -m 0644 "$ROOT/ops/systemd/dealix-hermes.timer" /etc/systemd/system/dealix-hermes.timer

chown -R "$DEPLOY_USER:$DEPLOY_USER" "$ROOT/docs/hermes" || true

systemctl daemon-reload
systemctl enable --now dealix-hermes.timer
systemctl start dealix-hermes.service || true
systemctl status dealix-hermes.timer --no-pager

echo "HERMES_SYSTEMD_INSTALL_OK"
