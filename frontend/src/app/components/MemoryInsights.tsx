'use client';

interface MemoryInsightsProps {
  memory: Record<string, unknown> | null;
  winnerReasoning?: string;
}

export default function MemoryInsights({ memory, winnerReasoning }: MemoryInsightsProps) {
  if (!memory) return null;

  const pastPurchases = (memory.past_purchases as Array<{ product: string; rating: number; note?: string }>) || [];
  const preferences = (memory.preferences as string[]) || [];
  const avoid = (memory.avoid as string[]) || [];
  const budgetPatterns = (memory.budget_patterns as Record<string, number>) || {};

  const hasSignals = pastPurchases.length > 0 || preferences.length > 0 || avoid.length > 0;
  if (!hasSignals) return null;

  return (
    <div className="glass-card agent-card animate-fade-in-up" id="memory-insights-card">
      <div className="agent-card-header">
        <div className="agent-card-title-row">
          <div className="agent-card-icon" style={{ background: 'rgba(139, 92, 246, 0.15)' }}>🧠</div>
          <span className="agent-card-title">Memory Insights</span>
        </div>
        <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>
          Cross-agent influence
        </span>
      </div>

      <div className="memory-insights">
        {preferences.length > 0 && (
          <div className="memory-item">
            <span className="memory-icon">💜</span>
            <span className="memory-text">
              <span className="memory-highlight">Preferred brands:</span>{' '}
              {preferences.join(', ')}
            </span>
          </div>
        )}

        {avoid.length > 0 && (
          <div className="memory-item" style={{ borderLeftColor: 'var(--accent-rose)' }}>
            <span className="memory-icon">🚫</span>
            <span className="memory-text">
              <span className="memory-highlight">Avoid list:</span>{' '}
              {avoid.join(', ')}
            </span>
          </div>
        )}

        {pastPurchases.length > 0 && (
          <div className="memory-item" style={{ borderLeftColor: 'var(--accent-cyan)' }}>
            <span className="memory-icon">📦</span>
            <span className="memory-text">
              <span className="memory-highlight">{pastPurchases.length} past purchase{pastPurchases.length !== 1 ? 's' : ''}</span>
              {' '}influencing analysis.{' '}
              {pastPurchases.filter(p => p.rating <= 2).length > 0 && (
                <>Negative experiences: {pastPurchases.filter(p => p.rating <= 2).map(p => p.product).join(', ')}.</>
              )}
            </span>
          </div>
        )}

        {Object.keys(budgetPatterns).length > 0 && (
          <div className="memory-item" style={{ borderLeftColor: 'var(--accent-emerald)' }}>
            <span className="memory-icon">📈</span>
            <span className="memory-text">
              <span className="memory-highlight">Budget patterns:</span>{' '}
              {Object.entries(budgetPatterns).map(([k, v]) => `${k}: $${v}`).join(', ')}
            </span>
          </div>
        )}

        {winnerReasoning && (
          <div className="memory-item" style={{ borderLeftColor: 'var(--accent-indigo)' }}>
            <span className="memory-icon">💡</span>
            <span className="memory-text" style={{ fontStyle: 'italic' }}>
              {winnerReasoning}
            </span>
          </div>
        )}
      </div>
    </div>
  );
}
