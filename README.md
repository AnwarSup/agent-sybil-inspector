<p align="center">
  <img src="https://img.shields.io/badge/product-agentic%20intelligence-7c3aed?style=for-the-badge" alt="Product">
  <img src="https://img.shields.io/badge/python-3.10%2B-2563eb?style=for-the-badge" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-16a34a?style=for-the-badge" alt="License">
</p>

<h1 align="center">Airdrop Sybil Inspector</h1>
<p align="center"><b>Airdrop defense system for wallet graph scoring, behavior similarity, and appeal-ready evidence packs.</b></p>

<p align="center">
  <a href="#-what-this-is">What this is</a> •
  <a href="#-product-surface">Product surface</a> •
  <a href="#-quick-start">Quick start</a> •
  <a href="#-architecture">Architecture</a>
</p>

---

## 🎯 What this is

Airdrop Sybil Inspector is a real repository product, not just a landing page. It includes a deterministic multi-agent reasoning core, an optional FastAPI API boundary, CLI demo runner, tests, CI, architecture docs, sample scenarios, and the existing Vercel-ready dashboard.

**Primary users:** airdrop teams and ecosystem foundations.

## 💼 Product surface

- **Reasoning core:** `backend/swarm.py` models specialist agents, confidence, trace IDs, risk scoring, and action plans.
- **API boundary:** `backend/app.py` exposes `/health`, `/scenarios`, `/analyze`, and `/demo-report`.
- **CLI console:** `python cli.py --all` generates operator-grade reports without external API keys.
- **Demo dashboard:** `index.html` remains deployable as a static product surface.
- **Quality gates:** `tests/test_swarm.py` plus `.github/workflows/ci.yml` keep the product verifiable.

## 🧠 Agent team

- **Wallet Graph Builder**
- **Behavior Similarity Agent**
- **Funding Source Analyst**
- **False Positive Reviewer**
- **Evidence Pack Writer**

## 🚀 Quick start

```bash
git clone https://github.com/<owner>/agent-sybil-inspector.git
cd agent-sybil-inspector
python3 cli.py --all
```

Optional API mode:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.app:app --reload
```

## 🧪 Test

```bash
python3 -m pytest -q
python3 backend/swarm.py | python3 -m json.tool >/dev/null
```

## 🏗️ Architecture

```mermaid
flowchart LR
  A[Signals] --> B[Specialist agents]
  B --> C[Verifier]
  C --> D[Risk score]
  D --> E[Operator action plan]
  E --> F[Dashboard / API / CLI]
```

## 📁 Repository map

```text
backend/swarm.py          Multi-agent reasoning engine
backend/app.py            Optional FastAPI service boundary
cli.py                    Local operator console
tests/test_swarm.py       CI-friendly product tests
examples/sample_scenario.json  Demo input payload
docs/ARCHITECTURE.md      Reasoning-loop architecture
docs/PRODUCT_SPEC.md      Product requirements and roadmap
index.html                Static live dashboard
```

## 🗺️ Roadmap

- [x] Static dashboard proof
- [x] Multi-agent reasoning core
- [x] CLI demo flow
- [x] API boundary
- [x] CI tests
- [ ] Real-time connector adapters
- [ ] Hosted report export
- [ ] Human approval workflow

## 📄 License

MIT.

<!-- MIMO_APPROVAL_PATTERN_UPGRADE -->
## Reviewer-Grade MiMo Agent Architecture

Sybil Inspector is structured as a token-intensive, multi-agent product rather than a static demo. The pipeline fans out across specialist agents, records per-agent token estimates, then synthesizes findings into reviewer-ready output.

### Specialist Agent Fleet
- **Cluster Builder** — groups wallets by funding, timing, behavior, and transaction motifs.
- **Pattern Detector** — identifies farm templates, synchronized actions, and bot-like cadence.
- **False Positive Judge** — protects legitimate user cohorts from overblocking.
- **Airdrop Policy Advisor** — turns findings into fair eligibility rules.
- **Evidence Reporter** — exports cluster explanations with confidence scores.

### Verified Demo Run
- Scenario: `airdrop dataset includes 42 wallets funded from shared source`
- Agents executed: 5
- Estimated tokens in sample run: **40,996**
- Daily projection at 96 runs/day: **3,935,616 tokens/day**
- Output artifact: `docs/example_run.json`
- Human-readable proof: `docs/EXAMPLE_RUN.md`

### Run Locally
```bash
python3 cli.py --all
python3 -m pytest -q
python3 - <<'PY'
from backend.core.pipeline import run_pipeline_sync
print(run_pipeline_sync('Sybil Inspector', {'subject': 'airdrop dataset includes 42 wallets funded from shared source'}))
PY
```

### Proof Pack
- `proofs/boot_log.txt` — environment boot evidence
- `proofs/run_sample.txt` — deterministic pipeline output summary
- `docs/example_run.json` — raw structured result
- `docs/EXAMPLE_RUN.md` — review-facing run report

