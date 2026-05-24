from backend.swarm import AGENT_ROLES, SCENARIOS, analyze_scenario, batch_analyze


def test_report_has_operator_grade_shape():
    report = analyze_scenario(SCENARIOS[0])
    data = report.to_dict()
    assert data['project'] == 'Airdrop Sybil Inspector'
    assert 0 <= data['risk_score'] <= 100
    assert data['verdict'] in {'operator_action_required', 'monitor_with_guardrails'}
    assert len(data['findings']) == len(AGENT_ROLES)
    assert data['trace_id']


def test_signal_override_changes_trace_and_keeps_schema():
    baseline = analyze_scenario(SCENARIOS[0]).to_dict()
    override = analyze_scenario(SCENARIOS[0], {'{SIGNAL}': 999 for SIGNAL in []}).to_dict()
    custom = analyze_scenario(SCENARIOS[0], {'{}'.format('funding_commonality'): 999}).to_dict()
    assert custom['trace_id'] != baseline['trace_id']
    assert len(custom['next_actions']) >= 3


def test_batch_covers_all_scenarios():
    reports = batch_analyze()
    assert len(reports) == len(SCENARIOS)
    assert {r['scenario'] for r in reports} == set(SCENARIOS)
