/**
 * Sybil Network Inspector — dApp Upgrade Wiring
 * Connects frontend to backend API, adds interactive features.
 */
(function() {
  'use strict';

  const API_BASE = (() => {
    const loc = window.location;
    // If served from FastAPI (port 8000), use same origin
    if (loc.port === '8000') return '';
    // Otherwise assume backend on :8000
    return loc.protocol + '//' + loc.hostname + ':8000';
  })();

  async function apiFetch(path, opts = {}) {
    try {
      const res = await fetch(API_BASE + path, {
        headers: { 'Content-Type': 'application/json' },
        ...opts
      });
      if (!res.ok) throw new Error(`API ${res.status}: ${res.statusText}`);
      return await res.json();
    } catch (e) {
      console.error('[Sybil Network Inspector] API error:', e);
      showToast('Backend unreachable — using local data', 'warning');
      return null;
    }
  }

  function showToast(msg, type = 'info') {
    let container = document.getElementById('toast-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'toast-container';
      container.style.cssText = 'position:fixed;top:16px;right:16px;z-index:9999;display:flex;flex-direction:column;gap:8px';
      document.body.appendChild(container);
    }
    const colors = { info: '#06b6d4', warning: '#eab308', error: '#ef4444', success: '#10b981' };
    const toast = document.createElement('div');
    toast.style.cssText = `padding:10px 16px;border-radius:8px;background:${colors[type] || colors.info}22;border:1px solid ${colors[type] || colors.info};color:#e2e8f0;font-size:13px;font-family:Inter,sans-serif;backdrop-filter:blur(8px)`;
    toast.textContent = msg;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), 4000);
  }

  // Health check on load
  async function checkHealth() {
    const data = await apiFetch('/health');
    if (data && data.status === 'ok') {
      showToast(`Backend connected: ${data.project}`, 'success');
      // Add health badge
      const badge = document.createElement('span');
      badge.className = 'badge';
      badge.style.cssText = 'background:#10b98133;color:#10b981;font-size:11px';
      badge.textContent = '🟢 API Connected';
      const header = document.querySelector('.flex.items-center.gap-3');
      if (header) header.appendChild(badge);
    }
  }

  // Load demo report from backend
  async function loadDemoReport() {
    const data = await apiFetch('/demo-report');
    if (!data) return;
    showToast(`Demo report loaded: ${data.length || 'ok'} scenarios`, 'info');
    return data;
  }

  // Chart.js integration
  function initChart(canvasId, config) {
    const canvas = document.getElementById(canvasId);
    if (!canvas || typeof Chart === 'undefined') return null;
    return new Chart(canvas.getContext('2d'), config);
  }

  // Export functions
  window.dappExportJSON = function(data, filename) {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename || '10-sybil-inspector-export.json';
    a.click();
    URL.revokeObjectURL(url);
    showToast('Exported JSON', 'success');
  };

  window.dappExportCSV = function(rows, filename) {
    if (!rows.length) return showToast('No data to export', 'warning');
    const headers = Object.keys(rows[0]);
    const csv = [headers.join(','), ...rows.map(r => headers.map(h => JSON.stringify(r[h] ?? '')).join(','))].join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename || '10-sybil-inspector-export.csv';
    a.click();
    URL.revokeObjectURL(url);
    showToast('Exported CSV', 'success');
  };

  // Wire existing buttons to backend API
  function wireButtons() {
    // Find all buttons with onclick containing fetch or analyze
    document.querySelectorAll('button[onclick]').forEach(btn => {
      const onclick = btn.getAttribute('onclick');
      // Leave existing onclick handlers intact
    });
  }

  // Add API status panel
  function addStatusPanel() {
    const panel = document.createElement('div');
    panel.className = 'panel p-3 mb-4';
    panel.style.cssText = 'border-color:#06b6d433';
    panel.innerHTML = `
      <div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap">
        <span id="api-status" style="font-size:12px;color:#94a3b8">⏳ Checking backend...</span>
        <button onclick="loadDemoReport()" class="btn btn-ghost" style="font-size:12px;padding:4px 10px">📊 Demo Report</button>
        <button onclick="checkHealth()" class="btn btn-ghost" style="font-size:12px;padding:4px 10px">🔄 Refresh</button>
      </div>
    `;
    const firstPanel = document.querySelector('.panel');
    if (firstPanel && firstPanel.parentNode) {
      firstPanel.parentNode.insertBefore(panel, firstPanel);
    }
  }

  // Init on DOM ready
  document.addEventListener('DOMContentLoaded', async () => {
    addStatusPanel();
    wireButtons();
    const health = await apiFetch('/health');
    const statusEl = document.getElementById('api-status');
    if (health && health.status === 'ok') {
      if (statusEl) statusEl.innerHTML = `🟢 <strong>${health.project}</strong> — ${health.agents} agents active`;
    } else {
      if (statusEl) statusEl.innerHTML = '🔴 Backend offline — UI running in standalone mode';
    }
  });

  // Expose API helpers globally
  window.dappAPI = { fetch: apiFetch, health: checkHealth, demoReport: loadDemoReport, toast: showToast, chart: initChart };

})();
