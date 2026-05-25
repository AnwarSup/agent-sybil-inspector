"""Token accounting for MiMo-style multi-agent workloads."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, List
from datetime import datetime, timezone

@dataclass
class TokenEvent:
    timestamp: str
    project: str
    agent: str
    estimated_tokens: int
    severity: str

class TokenTracker:
    def __init__(self, project: str):
        self.project = project
        self.events: List[TokenEvent] = []

    def record(self, agent: str, estimated_tokens: int, severity: str = "medium") -> None:
        self.events.append(TokenEvent(
            timestamp=datetime.now(timezone.utc).isoformat(),
            project=self.project,
            agent=agent,
            estimated_tokens=int(estimated_tokens),
            severity=severity,
        ))

    def snapshot(self) -> Dict[str, object]:
        total = sum(e.estimated_tokens for e in self.events)
        return {
            "project": self.project,
            "events": [asdict(e) for e in self.events],
            "total_estimated_tokens": total,
            "daily_projection_tokens": total * 96,
            "agent_count": len({e.agent for e in self.events}),
        }
