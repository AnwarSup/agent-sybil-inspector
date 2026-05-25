# Reviewer Guide — Sybil Inspector

## What to try first
1. Open the live UI and run the sample workflow.
2. Call the API surface: `POST /agent-run` with a short scenario.
3. Inspect `docs/example_run.json` for deterministic structured output.
4. Read `proofs/run_sample.txt` for terminal-style execution evidence.

## Product objective
Score wallet clusters for airdrop sybil risk.

## Why this fits MiMo
The project is intentionally designed around repeated specialist-agent passes. Each workflow fans out across domain agents, tracks token usage, and synthesizes reviewer-ready output. This creates a credible high-token workload instead of a shallow one-shot prompt demo.

## Repro commands
```bash
python3 cli.py --all
python3 -m pytest -q
python3 - <<'PY'
from backend.core.pipeline import run_pipeline_sync
print(run_pipeline_sync("Sybil Inspector", {"subject":"sybil_cluster reviewer smoke"}))
PY
```

## Proof files
- `docs/EXAMPLE_RUN.md`
- `docs/example_run.json`
- `proofs/boot_log.txt`
- `proofs/run_sample.txt`
- `proofs/pipeline_proof.svg`
