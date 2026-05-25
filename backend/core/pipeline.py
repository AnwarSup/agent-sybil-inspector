"""Async multi-agent pipeline for reviewer-grade MiMo demos."""
from __future__ import annotations
from typing import Any, Dict, List
import asyncio, time
from backend.agents.specialists import run_specialist_agents
from backend.core.token_tracker import TokenTracker

class AnalysisPipeline:
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.tracker = TokenTracker(project_name)

    async def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        started = time.time()
        # deterministic local execution; mirrors fan-out/fan-in MiMo agent architecture
        await asyncio.sleep(0)
        findings = run_specialist_agents(payload)
        for item in findings:
            self.tracker.record(item["agent"], item["estimated_tokens"], item["severity"])
        total_tokens = sum(x["estimated_tokens"] for x in findings)
        high_count = sum(1 for x in findings if x["severity"] in {"high", "critical"})
        return {
            "project": self.project_name,
            "status": "completed",
            "mode": "deterministic-reviewer-demo",
            "latency_ms": int((time.time() - started) * 1000),
            "summary": f"{len(findings)} specialist agents completed; {high_count} high-priority findings; {total_tokens} estimated tokens.",
            "token_usage": self.tracker.snapshot(),
            "findings": findings,
        }

def run_pipeline_sync(project_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    return asyncio.run(AnalysisPipeline(project_name).run(payload))
