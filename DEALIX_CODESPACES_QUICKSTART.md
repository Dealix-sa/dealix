# Dealix Codespaces Quickstart

## 1. Add API key safely

Best: GitHub → Settings → Codespaces → Secrets → New secret

Name:

OPENAI_API_KEY

Then restart Codespace.

Temporary terminal method:

export OPENAI_API_KEY="your_key_here"

## 2. Run API

./scripts/dealix-builder-dev.sh

## 3. Test API

In another terminal:

./scripts/dealix-api-test.sh

## 4. Use CLI

./scripts/dealix-builder.sh doctor
./scripts/dealix-builder.sh plan "Build Growth OS v6 inside dealix-v2 only"
./scripts/dealix-builder.sh founder-brief

## 5. Use Codex CLI in dealix-v2

./scripts/dealix-codex.sh "Improve Dealix CLI and add Growth OS commands. Stay inside dealix-v2."
