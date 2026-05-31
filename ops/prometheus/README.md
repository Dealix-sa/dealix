# Dealix Prometheus

This directory is reserved for self-hosted Prometheus configuration.

Recommended scrape targets for the Docker host:

- Prometheus itself
- node-exporter
- cAdvisor
- Dealix API metrics endpoint if enabled

Keep this configuration private to the Docker network and do not expose Prometheus directly to the public internet.
