'use client';

import { ExecutorResult } from '../types';

interface ResultPanelProps {
  execution: ExecutorResult | null;
}

export default function ResultPanel({ execution }: ResultPanelProps) {
  if (!execution) return null;

  const isPurchased = execution.status === 'PURCHASED';
  const icon = isPurchased ? '✅' : '❌';
  const statusColor = isPurchased ? 'var(--status-safe)' : 'var(--status-danger)';

  return (
    <div
      className="glass-card result-panel animate-fade-in-up"
      id="result-panel"
      style={{
        borderColor: isPurchased ? 'rgba(16, 185, 129, 0.2)' : 'rgba(244, 63, 94, 0.2)',
        background: isPurchased
          ? 'rgba(16, 185, 129, 0.03)'
          : 'rgba(244, 63, 94, 0.03)',
      }}
    >
      <div className="result-status-icon">{icon}</div>
      <div className="result-status-text" style={{ color: statusColor }}>
        {isPurchased ? 'PURCHASE EXECUTED' : 'PURCHASE REFUSED'}
      </div>
      <div className="result-reason">{execution.reason}</div>

      <div className="result-details">
        {execution.final_price != null && (
          <div className="result-detail-item">
            <span className="result-detail-label">Final Price</span>
            <span className="result-detail-value" style={{ color: statusColor }}>
              ${execution.final_price.toFixed(2)}
            </span>
          </div>
        )}
        {execution.tx_id && (
          <div className="result-detail-item">
            <span className="result-detail-label">Transaction</span>
            <span className="result-detail-value" style={{ fontSize: 13 }}>
              {execution.tx_id}
            </span>
          </div>
        )}
        {execution.wallet_balance != null && (
          <div className="result-detail-item">
            <span className="result-detail-label">Wallet Balance</span>
            <span className="result-detail-value">
              ${execution.wallet_balance.toFixed(2)}
            </span>
          </div>
        )}
      </div>
    </div>
  );
}
