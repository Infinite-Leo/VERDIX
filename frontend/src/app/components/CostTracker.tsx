'use client';

import { CostReport } from '../types';

interface CostTrackerProps {
  cost: CostReport | null;
}

export default function CostTracker({ cost }: CostTrackerProps) {
  if (!cost) return null;

  const items = [
    { label: 'Search (Exa)', value: cost.search_cost, icon: '🔍' },
    { label: 'AI Reasoning (OpenAI)', value: cost.ai_reasoning_cost, icon: '🧠' },
    { label: 'Negotiation Loop', value: cost.negotiation_cost, icon: '🤝' },
    { label: 'Wallet Check', value: cost.wallet_cost, icon: '💳' },
  ].filter(item => item.value > 0 || item.label === 'Search (Exa)');

  return (
    <div className="glass-card agent-card animate-fade-in-up" id="cost-tracker-card">
      <div className="agent-card-header">
        <div className="agent-card-title-row">
          <div className="agent-card-icon" style={{ background: 'rgba(245, 158, 11, 0.15)' }}>💸</div>
          <span className="agent-card-title">Agent Cost Tracker</span>
        </div>
        <span style={{ fontSize: 11, color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
          {cost.currency}
        </span>
      </div>
      <div className="cost-tracker">
        {items.map((item, i) => (
          <div className="cost-row" key={i}>
            <span className="cost-label">{item.icon} {item.label}</span>
            <span className="cost-value">${item.value.toFixed(4)}</span>
          </div>
        ))}
        <div className="cost-row">
          <span className="cost-label" style={{ fontWeight: 700, color: 'var(--text-primary)' }}>
            Total Decision Cost
          </span>
          <span className="cost-value cost-total">${cost.total.toFixed(4)}</span>
        </div>
      </div>
      <div style={{
        marginTop: 12,
        padding: '10px 12px',
        background: 'var(--accent-indigo-soft)',
        borderRadius: 'var(--radius-sm)',
        fontSize: 11,
        color: 'var(--text-accent)',
        textAlign: 'center',
        fontWeight: 500,
      }}>
        💡 This decision cost ${cost.total.toFixed(4)} in autonomous AI reasoning
      </div>
    </div>
  );
}
