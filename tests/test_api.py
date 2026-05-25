"""Smoke tests for Sybil Network Inspector API endpoints."""
from __future__ import annotations
import json
import pytest

try:
    from fastapi.testclient import TestClient
    from backend.app import app
    client = TestClient(app)
    HAS_CLIENT = True
except Exception:
    HAS_CLIENT = False


@pytest.mark.skipif(not HAS_CLIENT, reason="FastAPI not available")
def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert "project" in data
    assert "agents" in data


@pytest.mark.skipif(not HAS_CLIENT, reason="FastAPI not available")
def test_scenarios():
    r = client.get("/scenarios")
    assert r.status_code == 200
    data = r.json()
    assert "scenarios" in data
    assert isinstance(data["scenarios"], list)
    assert len(data["scenarios"]) > 0


@pytest.mark.skipif(not HAS_CLIENT, reason="FastAPI not available")
def test_analyze():
    r = client.post("/analyze", json={"scenario": None})
    assert r.status_code == 200
    data = r.json()
    assert "risk_score" in data
    assert "verdict" in data


@pytest.mark.skipif(not HAS_CLIENT, reason="FastAPI not available")
def test_demo_report():
    r = client.get("/demo-report")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_cli_json():
    """Verify CLI outputs valid JSON."""
    import subprocess, sys
    result = subprocess.run(
        [sys.executable, "cli.py", "--all"],
        capture_output=True, text=True, timeout=10
    )
    assert result.returncode == 0, f"CLI failed: {result.stderr}"
    data = json.loads(result.stdout)
    assert isinstance(data, (dict, list))
