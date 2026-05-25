from backend.core.pipeline import run_pipeline_sync


def test_agent_pipeline_contract():
    out = run_pipeline_sync("Sybil Inspector", {"subject": "sybil_cluster smoke scenario", "source": "pytest"})
    assert out["status"] == "completed"
    assert out["token_usage"]["total_estimated_tokens"] > 10000
    assert out["token_usage"]["agent_count"] >= 5
    assert len(out["findings"]) >= 5
    assert all("agent" in item and "recommendation" in item for item in out["findings"])
