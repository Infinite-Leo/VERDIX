'use client';

import { RiskProduct } from '../types';

interface AgentCardProps {
  products: RiskProduct[];
}

function getVerdictClass(verdict: string): string {
  return verdict === 'APPROVE' ? 'badge-approve' : 'badge-reject';
}

function getRiskClass(status: string): string {
  if (status === 'SAFE') return 'badge-safe';
  if (status === 'CAUTION') return 'badge-caution';
  return 'badge-danger';
}

export default function AgentCard({ products }: AgentCardProps) {
  if (!products || products.length === 0) {
    return (
      <div className="glass-card agent-card animate-fade-in-up" id="scout-results">
        <div className="agent-card-header">
          <div className="agent-card-title-row">
            <div className="agent-card-icon" style={{ background: 'rgba(6, 182, 212, 0.15)' }}>🔍</div>
            <span className="agent-card-title">Scout & Analysis</span>
          </div>
        </div>
        <p style={{ color: 'var(--text-muted)', fontSize: 13 }}>No products found for this query.</p>
      </div>
    );
  }

  return (
    <div className="glass-card agent-card animate-fade-in-up" id="scout-results">
      <div className="agent-card-header">
        <div className="agent-card-title-row">
          <div className="agent-card-icon" style={{ background: 'rgba(6, 182, 212, 0.15)' }}>🔍</div>
          <span className="agent-card-title">Scout & Analysis</span>
        </div>
        <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>
          {products.length} product{products.length !== 1 ? 's' : ''} found
        </span>
      </div>
      <div className="product-list stagger">
        {products.map((p, i) => (
          <div className="product-item" key={i} id={`product-${i}`}>
            <div className="product-info">
              <span className="product-name" title={p.name}>{p.name}</span>
              <span className="product-seller">{p.seller}</span>
            </div>
            <div className="product-meta">
              <span className={`product-score ${getVerdictClass(p.verdict)}`} style={{
                padding: '3px 8px',
                borderRadius: '100px',
                fontSize: 11,
                fontWeight: 700,
              }}>
                {p.verdict}
              </span>
              <span className={`product-score ${getRiskClass(p.risk_status)}`} style={{
                padding: '3px 8px',
                borderRadius: '100px',
                fontSize: 11,
                fontWeight: 700,
              }}>
                {p.risk_status} {p.risk_score}
              </span>
              <span className="product-price">
                ${p.price.toFixed(2)}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
