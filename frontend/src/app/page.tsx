'use client';

import { useState, useCallback } from 'react';
import PersonalityBar from './components/PersonalityBar';
import AgentFlow from './components/AgentFlow';
import AgentCard from './components/AgentCard';
import RiskMeter from './components/RiskMeter';
import NegotiationChat from './components/NegotiationChat';
import MemoryInsights from './components/MemoryInsights';
import CostTracker from './components/CostTracker';
import ConflictBanner from './components/ConflictBanner';
import ResultPanel from './components/ResultPanel';
import { Personality, AgentStep, PipelineResult } from './types';

const API_BASE = '';

export default function Home() {
  const [query, setQuery] = useState('');
  const [budget, setBudget] = useState('');
  const [personality, setPersonality] = useState<Personality>('balanced');
  const [currentStep, setCurrentStep] = useState<AgentStep>('idle');
  const [result, setResult] = useState<PipelineResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const runPipeline = useCallback(async () => {
    if (!query.trim()) return;

    setResult(null);
    setError(null);
    setCurrentStep('scout');

    // Simulate step progression for visual feedback
    const stepTimers = [
      setTimeout(() => setCurrentStep('analyst'), 1500),
      setTimeout(() => setCurrentStep('trust'), 3000),
      setTimeout(() => setCurrentStep('negotiator'), 4500),
      setTimeout(() => setCurrentStep('executor'), 7000),
    ];

    try {
      const response = await fetch(`${API_BASE}/api/run`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: query.trim(),
          budget: budget ? parseFloat(budget) : null,
          personality,
          user_id: 'default',
        }),
      });

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}));
        throw new Error(errData.detail || `API error: ${response.status}`);
      }

      const data: PipelineResult = await response.json();

      // Clear step timers and show final state
      stepTimers.forEach(clearTimeout);
      setCurrentStep('done');
      setResult(data);
    } catch (err) {
      stepTimers.forEach(clearTimeout);
      setCurrentStep('error');
      setError(err instanceof Error ? err.message : 'An unexpected error occurred');
    }
  }, [query, budget, personality]);

  const isLoading = currentStep !== 'idle' && currentStep !== 'done' && currentStep !== 'error';

  return (
    <div className="app-container">
      {/* Header */}
      <header className="header" id="header">
        <div className="header-brand">
          <div className="header-logo">V</div>
          <div>
            <div className="header-title">VERDIX</div>
            <div className="header-subtitle">Autonomous Financial Decision Engine</div>
          </div>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          {result?.demo_mode && (
            <div className="header-badge" style={{
              background: 'rgba(245, 158, 11, 0.12)',
              borderColor: 'rgba(245, 158, 11, 0.3)',
              color: 'var(--accent-amber)',
            }}>
              🧪 Demo Mode
            </div>
          )}
          <div className="header-badge">
            <span className="header-badge-dot" />
            Locus Beta
          </div>
        </div>
      </header>

      {/* Input Section */}
      <section className="input-section" id="input-section">
        <div className="glass-card input-card">
          <div style={{ marginBottom: 16 }}>
            <div className="input-label" style={{ marginBottom: 8 }}>Agent Personality</div>
            <PersonalityBar personality={personality} onChange={setPersonality} />
          </div>
          <div className="input-row">
            <div className="input-group">
              <label className="input-label" htmlFor="query-input">What should VERDIX decide?</label>
              <input
                id="query-input"
                className="input-field"
                type="text"
                placeholder="e.g. Buy gaming mouse under ₹2000"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && !isLoading && runPipeline()}
                disabled={isLoading}
              />
            </div>
            <div className="input-group" style={{ maxWidth: 140 }}>
              <label className="input-label" htmlFor="budget-input">Budget (USD)</label>
              <input
                id="budget-input"
                className="input-field"
                type="number"
                placeholder="Optional"
                value={budget}
                onChange={(e) => setBudget(e.target.value)}
                disabled={isLoading}
              />
            </div>
            <button
              className="run-btn"
              onClick={runPipeline}
              disabled={isLoading || !query.trim()}
              id="run-pipeline-btn"
            >
              {isLoading ? (
                <span className="run-btn-loading">
                  <span className="spinner" />
                  Analyzing...
                </span>
              ) : (
                '⚡ Run VERDIX'
              )}
            </button>
          </div>
        </div>
      </section>

      {/* Agent Flow */}
      {currentStep !== 'idle' && <AgentFlow currentStep={currentStep} />}

      {/* Error */}
      {error && (
        <div className="conflict-banner danger animate-fade-in-up" style={{ marginBottom: 24 }} id="error-banner">
          <span className="conflict-icon">❌</span>
          <div className="conflict-content">
            <div className="conflict-title" style={{ color: 'var(--status-danger)' }}>Pipeline Error</div>
            <div className="conflict-desc">{error}</div>
          </div>
        </div>
      )}

      {/* Loading Skeleton */}
      {isLoading && !result && (
        <div className="results-grid" style={{ marginBottom: 24 }}>
          <div className="glass-card agent-card results-full animate-fade-in">
            <div style={{ padding: 8 }}>
              <div className="skeleton skeleton-line long" />
              <div className="skeleton skeleton-line medium" />
              <div className="skeleton skeleton-line short" />
              <div className="skeleton skeleton-line long" style={{ marginTop: 16 }} />
              <div className="skeleton skeleton-line medium" />
            </div>
          </div>
        </div>
      )}

      {/* Results */}
      {result && (
        <>
          {/* Conflict Banner */}
          {result.conflict && result.conflict.has_conflict && (
            <div style={{ marginBottom: 20 }}>
              <ConflictBanner conflict={result.conflict} />
            </div>
          )}

          {/* Main Grid */}
          <div className="results-grid">
            {/* Scout & Analyst Results (full width) */}
            <div className="results-full">
              <AgentCard products={result.products} />
            </div>

            {/* Risk Meter */}
            <RiskMeter product={result.winner || (result.products.length > 0 ? result.products[0] : null)} />

            {/* Negotiation Chat */}
            <NegotiationChat negotiation={result.negotiation || null} />

            {/* Memory Insights */}
            <MemoryInsights
              memory={result.memory_used || null}
              winnerReasoning={result.winner?.reasoning}
            />

            {/* Cost Tracker */}
            <CostTracker cost={result.cost} />

            {/* Result Panel (full width) */}
            <div className="results-full">
              <ResultPanel execution={result.execution} />
            </div>
          </div>

          {/* Aligned Agents Banner */}
          {result.conflict && !result.conflict.has_conflict && (
            <div style={{ marginTop: -4, marginBottom: 20 }}>
              <ConflictBanner conflict={result.conflict} />
            </div>
          )}
        </>
      )}

      {/* Empty State */}
      {currentStep === 'idle' && !result && (
        <div className="empty-state" id="empty-state">
          <div className="empty-state-icon">⚖️</div>
          <div className="empty-state-title">Ready to Judge</div>
          <div className="empty-state-desc">
            Enter a purchase query above and VERDIX will autonomously scout, analyze, assess risk, negotiate, and decide — with full cost transparency.
          </div>
        </div>
      )}
    </div>
  );
}
