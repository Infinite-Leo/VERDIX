'use client';

import { NegotiationResult } from '../types';

interface NegotiationChatProps {
  negotiation: NegotiationResult | null;
}

export default function NegotiationChat({ negotiation }: NegotiationChatProps) {
  if (!negotiation || negotiation.turns.length === 0) {
    return (
      <div className="glass-card agent-card animate-fade-in-up" id="negotiation-card">
        <div className="agent-card-header">
          <div className="agent-card-title-row">
            <div className="agent-card-icon" style={{ background: 'rgba(139, 92, 246, 0.15)' }}>🤝</div>
            <span className="agent-card-title">Negotiation</span>
          </div>
        </div>
        <p style={{ color: 'var(--text-muted)', fontSize: 13 }}>
          No negotiation was conducted for this decision.
        </p>
      </div>
    );
  }

  return (
    <div className="glass-card agent-card animate-fade-in-up" id="negotiation-card">
      <div className="agent-card-header">
        <div className="agent-card-title-row">
          <div className="agent-card-icon" style={{ background: 'rgba(139, 92, 246, 0.15)' }}>🤝</div>
          <span className="agent-card-title">Negotiation Loop</span>
        </div>
        <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>
          {negotiation.personality_used} mode
        </span>
      </div>

      <div className="negotiation-chat">
        {negotiation.turns.map((turn, i) => (
          <div
            className={`chat-bubble ${turn.role}`}
            key={i}
            style={{ animationDelay: `${i * 0.15}s` }}
            id={`chat-turn-${i}`}
          >
            <div className={`chat-role ${turn.role}`}>
              {turn.role === 'seller' ? '🏪 Seller' : '🤖 VERDIX Agent'}
            </div>
            {turn.message.length > 300 ? turn.message.slice(0, 300) + '...' : turn.message}
          </div>
        ))}
      </div>

      {negotiation.savings > 0 && (
        <div className="chat-savings" id="negotiation-savings">
          <span style={{ fontSize: 16 }}>💸</span>
          <span className="chat-savings-label">Negotiated Savings</span>
          <span className="chat-savings-amount">${negotiation.savings.toFixed(2)}</span>
        </div>
      )}

      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        marginTop: 12,
        padding: '10px 0 0',
        borderTop: '1px solid var(--border-subtle)',
        fontSize: 13,
        color: 'var(--text-muted)',
      }}>
        <span>Original: <strong style={{ color: 'var(--text-secondary)' }}>${negotiation.original_price.toFixed(2)}</strong></span>
        <span>Final: <strong style={{ color: 'var(--status-safe)' }}>${negotiation.final_price.toFixed(2)}</strong></span>
      </div>
    </div>
  );
}
