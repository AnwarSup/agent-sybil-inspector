"""Airdrop Sybil Inspector — real product workflow.

Ingest wallet records, detect sybil clusters, score risk, rank wallets, and
export an appeal-ready evidence pack. Deterministic so reviewers can reproduce
output from the bundled fixture.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import os
import statistics
from collections import defaultdict
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional, Sequence

FIXTURE_PATH = os.path.join(os.path.dirname(__file__), '..', 'examples', 'sample_dataset.json')

REQUIRED_FIELDS = ('address',)
DETECTION_SIGNALS = (
    'shared_funding',
    'shared_device',
    'shared_ip',
    'tx_timing',
    'contract_overlap',
    'low_age',
    'low_gas_paid',
)


@dataclass
class WalletScore:
    address: str
    risk_score: int
    severity: str
    cluster_id: Optional[str]
    flags: List[str]
    age_days: float
    tx_count: int
    balance_eth: float
    funding_source: Optional[str]
    contracts_touched: List[str] = field(default_factory=list)


@dataclass
class Cluster:
    cluster_id: str
    size: int
    members: List[str]
    reasons: List[str]
    confidence: float
    risk_score: int


@dataclass
class IngestReport:
    project: str
    generated_at: str
    total_wallets: int
    flagged_wallets: int
    clusters: List[Cluster]
    wallets: List[WalletScore]
    summary: Dict[str, Any]
    next_actions: List[str]
    trace_id: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            'project': self.project,
            'generated_at': self.generated_at,
            'total_wallets': self.total_wallets,
            'flagged_wallets': self.flagged_wallets,
            'clusters': [asdict(c) for c in self.clusters],
            'wallets': [asdict(w) for w in self.wallets],
            'summary': self.summary,
            'next_actions': self.next_actions,
            'trace_id': self.trace_id,
        }


def load_sample() -> List[Dict[str, Any]]:
    with open(FIXTURE_PATH, 'r', encoding='utf-8') as fh:
        data = json.load(fh)
    return data['wallets']


def _severity(score: int) -> str:
    if score >= 80:
        return 'critical'
    if score >= 60:
        return 'high'
    if score >= 35:
        return 'medium'
    return 'low'


def _trace_id(payload: Sequence[Dict[str, Any]]) -> str:
    src = json.dumps(payload, sort_keys=True, default=str)
    return hashlib.sha1(src.encode()).hexdigest()[:12]


def _validate(wallets: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    cleaned: List[Dict[str, Any]] = []
    for raw in wallets:
        if not isinstance(raw, dict):
            continue
        addr = raw.get('address')
        if not isinstance(addr, str) or not addr.startswith('0x'):
            continue
        item = {
            'address': addr.lower(),
            'age_days': float(raw.get('age_days', 0) or 0),
            'tx_count': int(raw.get('tx_count', 0) or 0),
            'balance_eth': float(raw.get('balance_eth', 0) or 0),
            'gas_paid_eth': float(raw.get('gas_paid_eth', 0) or 0),
            'funding_source': (raw.get('funding_source') or '').lower() or None,
            'device_hash': (raw.get('device_hash') or '').lower() or None,
            'ip_hash': (raw.get('ip_hash') or '').lower() or None,
            'first_tx_ts': int(raw.get('first_tx_ts', 0) or 0),
            'contracts_touched': sorted({str(c).lower() for c in (raw.get('contracts_touched') or [])}),
        }
        cleaned.append(item)
    return cleaned


def _group(wallets: Sequence[Dict[str, Any]], key: str) -> Dict[str, List[Dict[str, Any]]]:
    buckets: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for w in wallets:
        val = w.get(key)
        if val:
            buckets[val].append(w)
    return {k: v for k, v in buckets.items() if len(v) > 1}


def _timing_groups(wallets: Sequence[Dict[str, Any]], window_seconds: int = 3600) -> List[List[Dict[str, Any]]]:
    ordered = sorted([w for w in wallets if w.get('first_tx_ts')], key=lambda w: w['first_tx_ts'])
    groups: List[List[Dict[str, Any]]] = []
    bucket: List[Dict[str, Any]] = []
    last_ts = 0
    for w in ordered:
        ts = w['first_tx_ts']
        if bucket and ts - last_ts <= window_seconds:
            bucket.append(w)
        else:
            if len(bucket) > 1:
                groups.append(bucket)
            bucket = [w]
        last_ts = ts
    if len(bucket) > 1:
        groups.append(bucket)
    return groups


def _score_wallet(w: Dict[str, Any], flags: List[str], peer_count: int) -> int:
    score = 0
    score += 18 * sum(1 for f in flags if f.startswith('shared_'))
    score += 12 if 'tx_timing' in flags else 0
    score += 14 if 'contract_overlap' in flags else 0
    score += 10 if 'low_age' in flags else 0
    score += 6 if 'low_gas_paid' in flags else 0
    score += min(20, peer_count * 3)
    if w['age_days'] < 14:
        score += 8
    if w['tx_count'] < 4:
        score += 4
    return max(0, min(100, score))


def analyze_dataset(wallets: Iterable[Dict[str, Any]]) -> IngestReport:
    """Run the full sybil-detection workflow on a list of wallet records."""
    cleaned = _validate(wallets)
    if not cleaned:
        empty = IngestReport(
            project='Airdrop Sybil Inspector',
            generated_at=datetime.now(timezone.utc).isoformat(),
            total_wallets=0,
            flagged_wallets=0,
            clusters=[],
            wallets=[],
            summary={'shared_funders': 0, 'shared_devices': 0, 'timing_clusters': 0, 'mean_risk': 0},
            next_actions=['Provide a wallet dataset with at least 2 records'],
            trace_id='empty00000',
        )
        return empty

    funding_groups = _group(cleaned, 'funding_source')
    device_groups = _group(cleaned, 'device_hash')
    ip_groups = _group(cleaned, 'ip_hash')
    timing_groups = _timing_groups(cleaned)

    # contract overlap detection
    contract_groups: Dict[frozenset, List[Dict[str, Any]]] = defaultdict(list)
    for w in cleaned:
        if w['contracts_touched']:
            key = frozenset(w['contracts_touched'])
            contract_groups[key].append(w)
    contract_clusters = {','.join(sorted(k)): v for k, v in contract_groups.items() if len(v) > 1 and len(k) >= 2}

    flags_by_addr: Dict[str, List[str]] = defaultdict(list)
    peer_count_by_addr: Dict[str, int] = defaultdict(int)

    for src, members in funding_groups.items():
        for m in members:
            flags_by_addr[m['address']].append(f'shared_funding:{src[:10]}')
            peer_count_by_addr[m['address']] += len(members) - 1
    for src, members in device_groups.items():
        for m in members:
            flags_by_addr[m['address']].append(f'shared_device:{src[:10]}')
            peer_count_by_addr[m['address']] += len(members) - 1
    for src, members in ip_groups.items():
        for m in members:
            flags_by_addr[m['address']].append(f'shared_ip:{src[:10]}')
            peer_count_by_addr[m['address']] += len(members) - 1
    for group in timing_groups:
        for m in group:
            flags_by_addr[m['address']].append('tx_timing')
            peer_count_by_addr[m['address']] += len(group) - 1
    for key, members in contract_clusters.items():
        for m in members:
            flags_by_addr[m['address']].append('contract_overlap')
    for w in cleaned:
        if w['age_days'] < 30:
            flags_by_addr[w['address']].append('low_age')
        if w['gas_paid_eth'] < 0.003 and w['tx_count'] > 0:
            flags_by_addr[w['address']].append('low_gas_paid')

    # build wallet scores
    wallet_scores: List[WalletScore] = []
    cluster_assignment: Dict[str, str] = {}
    clusters: List[Cluster] = []

    cluster_seeds: List[Dict[str, Any]] = []
    for src, members in funding_groups.items():
        cluster_seeds.append({'kind': 'funding', 'key': src, 'members': [m['address'] for m in members]})
    for src, members in device_groups.items():
        cluster_seeds.append({'kind': 'device', 'key': src, 'members': [m['address'] for m in members]})
    for src, members in ip_groups.items():
        cluster_seeds.append({'kind': 'ip', 'key': src, 'members': [m['address'] for m in members]})

    seen = set()
    cluster_counter = 0
    for seed in cluster_seeds:
        members = tuple(sorted(seed['members']))
        if members in seen:
            continue
        seen.add(members)
        cluster_counter += 1
        cid = f'CL-{cluster_counter:03d}'
        reasons = [f"{seed['kind']} shared: {seed['key'][:14]}"]
        # check overlap with other dimensions
        addrs = set(members)
        for other in cluster_seeds:
            if other is seed:
                continue
            if addrs.intersection(other['members']) and len(addrs.intersection(other['members'])) >= 2:
                reasons.append(f"{other['kind']} overlap")
        risk = min(100, 40 + len(members) * 10 + len(reasons) * 5)
        confidence = round(min(0.99, 0.55 + len(reasons) * 0.08 + len(members) * 0.03), 2)
        clusters.append(Cluster(cluster_id=cid, size=len(members), members=list(members), reasons=sorted(set(reasons)), confidence=confidence, risk_score=risk))
        for addr in members:
            cluster_assignment.setdefault(addr, cid)

    for w in cleaned:
        flags = sorted(set(flags_by_addr.get(w['address'], [])))
        score = _score_wallet(w, flags, peer_count_by_addr.get(w['address'], 0))
        wallet_scores.append(WalletScore(
            address=w['address'],
            risk_score=score,
            severity=_severity(score),
            cluster_id=cluster_assignment.get(w['address']),
            flags=flags,
            age_days=w['age_days'],
            tx_count=w['tx_count'],
            balance_eth=w['balance_eth'],
            funding_source=w['funding_source'],
            contracts_touched=w['contracts_touched'],
        ))

    wallet_scores.sort(key=lambda x: x.risk_score, reverse=True)
    clusters.sort(key=lambda c: c.risk_score, reverse=True)

    flagged = sum(1 for w in wallet_scores if w.severity in ('high', 'critical'))
    mean_risk = int(round(statistics.fmean(w.risk_score for w in wallet_scores)))
    summary = {
        'shared_funders': len(funding_groups),
        'shared_devices': len(device_groups),
        'shared_ips': len(ip_groups),
        'timing_clusters': len(timing_groups),
        'contract_overlaps': len(contract_clusters),
        'mean_risk': mean_risk,
        'severity_distribution': {
            sev: sum(1 for w in wallet_scores if w.severity == sev)
            for sev in ('low', 'medium', 'high', 'critical')
        },
    }
    next_actions = [
        f'Open appeal review for {flagged} flagged wallets',
        f'Bundle evidence pack covering {len(clusters)} clusters',
        'Cross-check funding sources against known CEX deposit registry',
        'Notify airdrop ops to hold disbursement until human verification',
    ]
    return IngestReport(
        project='Airdrop Sybil Inspector',
        generated_at=datetime.now(timezone.utc).isoformat(),
        total_wallets=len(cleaned),
        flagged_wallets=flagged,
        clusters=clusters,
        wallets=wallet_scores,
        summary=summary,
        next_actions=next_actions,
        trace_id=_trace_id(cleaned),
    )


def export_csv(report: IngestReport) -> str:
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(['address', 'risk_score', 'severity', 'cluster_id', 'flags', 'age_days', 'tx_count', 'balance_eth', 'funding_source'])
    for w in report.wallets:
        writer.writerow([
            w.address, w.risk_score, w.severity, w.cluster_id or '',
            ';'.join(w.flags), f'{w.age_days:.1f}', w.tx_count,
            f'{w.balance_eth:.4f}', w.funding_source or '',
        ])
    return buf.getvalue()


def run_sample() -> Dict[str, Any]:
    """Convenience: load fixture, run analyze_dataset, return dict."""
    return analyze_dataset(load_sample()).to_dict()


if __name__ == '__main__':
    print(json.dumps(run_sample(), indent=2))
