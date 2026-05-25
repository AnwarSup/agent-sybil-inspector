# Example Run — Sybil Inspector

This artifact records a deterministic reviewer demo run for the MiMo approval pattern.

- Project: **Sybil Inspector**
- Domain: sybil risk analysis
- Scenario: `airdrop dataset includes 42 wallets funded from shared source`
- Status: `completed`
- Mode: `deterministic-reviewer-demo`
- Specialist agents: 5
- Estimated tokens: **40,996**
- Daily projection: **3,935,616 tokens/day**

## Findings

### Liquidity Scout
- Role: tracks pool depth, volatility spikes, and suspicious flow concentration
- Severity: `critical`
- Confidence: `0.69`
- Estimated tokens: `10795`
- Finding: Liquidity Scout reviewed DeFi risk monitoring signal: airdrop dataset includes 42 wallets funded from shared source. Risk pattern=critical confidence=0.69.
- Recommendation: Run liquidity scout follow-up pass, capture artifacts, then prioritize critical items first.

### Exploit Sentinel
- Role: maps events to known attack primitives and detects anomalous protocol behavior
- Severity: `low`
- Confidence: `0.82`
- Estimated tokens: `4656`
- Finding: Exploit Sentinel reviewed DeFi risk monitoring signal: airdrop dataset includes 42 wallets funded from shared source. Risk pattern=low confidence=0.82.
- Recommendation: Run exploit sentinel follow-up pass, capture artifacts, then prioritize low items first.

### Oracle Auditor
- Role: checks oracle drift, stale feeds, and manipulation windows
- Severity: `high`
- Confidence: `0.89`
- Estimated tokens: `5530`
- Finding: Oracle Auditor reviewed DeFi risk monitoring signal: airdrop dataset includes 42 wallets funded from shared source. Risk pattern=high confidence=0.89.
- Recommendation: Run oracle auditor follow-up pass, capture artifacts, then prioritize high items first.

### Treasury Guardian
- Role: scores treasury exposure and proposes emergency controls
- Severity: `critical`
- Confidence: `0.88`
- Estimated tokens: `9263`
- Finding: Treasury Guardian reviewed DeFi risk monitoring signal: airdrop dataset includes 42 wallets funded from shared source. Risk pattern=critical confidence=0.88.
- Recommendation: Run treasury guardian follow-up pass, capture artifacts, then prioritize critical items first.

### Incident Reporter
- Role: synthesizes operator-grade markdown incident reports
- Severity: `low`
- Confidence: `0.85`
- Estimated tokens: `10752`
- Finding: Incident Reporter reviewed DeFi risk monitoring signal: airdrop dataset includes 42 wallets funded from shared source. Risk pattern=low confidence=0.85.
- Recommendation: Run incident reporter follow-up pass, capture artifacts, then prioritize low items first.

