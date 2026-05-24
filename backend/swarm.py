"""Airdrop Sybil Inspector multi-agent reasoning core.

This module is intentionally dependency-light so the product can run in CI,
inside a static demo, or behind the optional FastAPI boundary without needing
external model keys. It models the decision loop real AI agents would use:
observe signals, let specialist agents reason, verify the result, then emit an
operator-ready action plan.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import hashlib
import json
import statistics
from typing import Any, Dict, Iterable, List

PROJECT_NAME = 'Airdrop Sybil Inspector'
DOMAIN = 'anti-fraud intelligence'
AUDIENCE = 'airdrop teams and ecosystem foundations'
AGENT_ROLES = ['Wallet Graph Builder', 'Behavior Similarity Agent', 'Funding Source Analyst', 'False Positive Reviewer', 'Evidence Pack Writer']
SIGNALS = ['funding_commonality', 'tx_timing_similarity', 'contract_touch_overlap', 'device_proxy_risk', 'appeal_confidence']
SCENARIOS = ['airdrop eligibility screening', 'cluster appeal review', 'campaign fraud audit']


@dataclass(frozen=True)
class AgentFinding:
    agent: str
    severity: str
    confidence: float
    observation: str
    recommendation: str


@dataclass(frozen=True)
class SwarmReport:
    project: str
    domain: str
    scenario: str
    risk_score: int
    confidence: float
    verdict: str
    findings: List[AgentFinding]
    next_actions: List[str]
    trace_id: str
    generated_at: str

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['findings'] = [asdict(f) for f in self.findings]
        return data


def _normalize(values: Iterable[float]) -> float:
    vals = [max(0.0, float(v)) for v in values]
    if not vals:
        return 0.0
    peak = max(vals) or 1.0
    return min(1.0, statistics.fmean(vals) / peak)


def _severity(score: float) -> str:
    if score >= 0.78:
        return 'critical'
    if score >= 0.55:
        return 'high'
    if score >= 0.32:
        return 'medium'
    return 'low'


def _default_signal_value(signal: str, scenario: str, idx: int) -> float:
    digest = hashlib.sha256(f'{PROJECT_NAME}:{scenario}:{signal}'.encode()).hexdigest()
    return 20 + (int(digest[:6], 16) % 80) + idx * 3


def analyze_scenario(scenario: str | None = None, signals: Dict[str, float] | None = None) -> SwarmReport:
    """Run a deterministic specialist-agent analysis for one scenario."""
    scenario = scenario or SCENARIOS[0]
    provided = signals or {}
    signal_values = {s: float(provided.get(s, _default_signal_value(s, scenario, i))) for i, s in enumerate(SIGNALS)}
    normalized = _normalize(signal_values.values())
    risk_score = int(round(normalized * 100))

    findings: List[AgentFinding] = []
    for i, agent in enumerate(AGENT_ROLES):
        signal = SIGNALS[i % len(SIGNALS)]
        raw = signal_values[signal]
        local_score = min(1.0, (raw / (max(signal_values.values()) or 1.0)) * (0.82 + i * 0.035))
        sev = _severity(local_score)
        confidence = round(0.62 + min(0.32, local_score / 3), 2)
        findings.append(AgentFinding(
            agent=agent,
            severity=sev,
            confidence=confidence,
            observation=f'{signal} is reading {raw:.2f} during {scenario}.',
            recommendation=f'Prioritize {agent.lower()} workflow; verify {signal} before execution.'
        ))

    criticals = sum(1 for f in findings if f.severity in ('critical', 'high'))
    verdict = 'operator_action_required' if risk_score >= 65 or criticals >= 2 else 'monitor_with_guardrails'
    next_actions = [
        f'Open {scenario} incident room for {AUDIENCE}',
        f'Assign {findings[0].agent} and {findings[1].agent} as primary reviewers',
        'Export evidence pack with raw signals, assumptions, and confidence scores',
        'Schedule follow-up verification after next telemetry interval',
    ]
    trace_src = json.dumps({'project': PROJECT_NAME, 'scenario': scenario, 'signals': signal_values}, sort_keys=True)
    trace_id = hashlib.sha1(trace_src.encode()).hexdigest()[:12]
    confidence = round(statistics.fmean(f.confidence for f in findings), 2)
    return SwarmReport(
        project=PROJECT_NAME,
        domain=DOMAIN,
        scenario=scenario,
        risk_score=risk_score,
        confidence=confidence,
        verdict=verdict,
        findings=findings,
        next_actions=next_actions,
        trace_id=trace_id,
        generated_at=datetime.now(timezone.utc).isoformat(),
    )


def batch_analyze() -> List[Dict[str, Any]]:
    """Analyze all built-in scenarios; useful for demos, tests, and smoke checks."""
    return [analyze_scenario(s).to_dict() for s in SCENARIOS]


if __name__ == '__main__':
    print(json.dumps(batch_analyze(), indent=2))
