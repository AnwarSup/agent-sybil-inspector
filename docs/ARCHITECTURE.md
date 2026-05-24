# Airdrop Sybil Inspector Architecture

## Purpose

Airdrop defense system for wallet graph scoring, behavior similarity, and appeal-ready evidence packs.

## Runtime loop

1. **Observe** — collect domain signals: funding_commonality, tx_timing_similarity, contract_touch_overlap, device_proxy_risk, appeal_confidence.
2. **Orient** — map the active scenario to specialist agent responsibilities.
3. **Decide** — score severity, confidence, and operator urgency.
4. **Act** — emit next actions that a human operator can verify.
5. **Reflect** — attach trace IDs and deterministic evidence for review.

## Components

- `backend/swarm.py` — pure Python reasoning core, safe for CI and static demos.
- `backend/app.py` — FastAPI wrapper for product integration.
- `cli.py` — terminal demo path for reviewers.
- `index.html` — front-facing dashboard surface.

## Agent responsibilities

- `Wallet Graph Builder`: owns one part of the analysis loop.
- `Behavior Similarity Agent`: owns one part of the analysis loop.
- `Funding Source Analyst`: owns one part of the analysis loop.
- `False Positive Reviewer`: owns one part of the analysis loop.
- `Evidence Pack Writer`: owns one part of the analysis loop.

## Production extension points

- Replace deterministic signals with live connectors.
- Persist reports in Postgres or SQLite.
- Add auth and organization workspaces.
- Add export hooks for Slack, Discord, Telegram, or email.
