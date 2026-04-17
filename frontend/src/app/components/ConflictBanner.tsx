'use client';

import { ConflictReport } from '../types';

interface ConflictBannerProps {
  conflict: ConflictReport | null;
}

export default function ConflictBanner({ conflict }: ConflictBannerProps) {
  if (!conflict) return null;

  const variant = conflict.has_conflict
    ? conflict.conflict_type === 'VALUE_VS_RISK'
      ? 'danger'
      : 'warning'
    : 'safe';

  const icon = conflict.has_conflict ? (variant === 'danger' ? '🚨' : '⚠️') : '✅';

  const title = conflict.has_conflict
    ? `Conflict Detected: ${conflict.conflict_type.replace(/_/g, ' ')}`
    : 'Agents Aligned';

  return (
    <div className={`conflict-banner ${variant}`} id="conflict-banner">
      <span className="conflict-icon">{icon}</span>
      <div className="conflict-content">
        <div className="conflict-title" style={{
          color: variant === 'danger' ? 'var(--status-danger)' :
                 variant === 'warning' ? 'var(--status-caution)' :
                 'var(--status-safe)'
        }}>
          {title}
        </div>
        <div className="conflict-desc">{conflict.description}</div>
        <div className="conflict-rec">💡 {conflict.recommendation}</div>
      </div>
    </div>
  );
}
