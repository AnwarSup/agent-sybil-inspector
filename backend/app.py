"""Optional FastAPI boundary for Airdrop Sybil Inspector."""
from __future__ import annotations

try:
    from fastapi import FastAPI
    from pydantic import BaseModel, Field
except Exception:  # pragma: no cover - keeps core importable without web deps
    FastAPI = None
    BaseModel = object
    def Field(default=None, **_: object):
        return default

from .swarm import PROJECT_NAME, DOMAIN, AGENT_ROLES, SCENARIOS, analyze_scenario, batch_analyze

if FastAPI:
    app = FastAPI(title=PROJECT_NAME, version='1.0.0', description=f'{PROJECT_NAME} API for {DOMAIN}')

    class AnalyzeRequest(BaseModel):
        scenario: str | None = Field(default=None, description='Scenario name to analyze')
        signals: dict[str, float] = Field(default_factory=dict, description='Optional signal overrides')

    @app.get('/health')
    def health():
        return {'status': 'ok', 'project': PROJECT_NAME, 'agents': len(AGENT_ROLES)}

    @app.get('/scenarios')
    def scenarios():
        return {'scenarios': SCENARIOS, 'agents': AGENT_ROLES}

    @app.post('/analyze')
    def analyze(req: AnalyzeRequest):
        return analyze_scenario(req.scenario, req.signals).to_dict()

    @app.get('/demo-report')
    def demo_report():
        return batch_analyze()
else:
    app = None
