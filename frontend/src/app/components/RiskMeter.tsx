'use client';

import { RiskProduct } from '../types';

interface RiskMeterProps {
  product: RiskProduct | null;
}

export default function RiskMeter({ product }: RiskMeterProps) {
  if (!product) return null;

  const { risk_score, risk_status, risk_flags } = product;

  // Arc geometry
  const cx = 100;
  const cy = 100;
  const r = 80;
  const startAngle = Math.PI; // 180 degrees (left)
  const endAngle = 0; // 0 degrees (right)
  const totalAngle = Math.PI;
  const filledAngle = (risk_score / 100) * totalAngle;

  // Background arc path (full semicircle)
  const bgStartX = cx + r * Math.cos(startAngle);
  const bgStartY = cy - r * Math.sin(startAngle);
  const bgEndX = cx + r * Math.cos(endAngle);
  const bgEndY = cy - r * Math.sin(endAngle);
  const bgPath = `M ${bgStartX} ${bgStartY} A ${r} ${r} 0 0 1 ${bgEndX} ${bgEndY}`;

  // Filled arc path
  const fillEndAngle = startAngle - filledAngle;
  const fillEndX = cx + r * Math.cos(fillEndAngle);
  const fillEndY = cy - r * Math.sin(fillEndAngle);
  const largeArc = filledAngle > Math.PI ? 1 : 0;
  const fillPath = `M ${bgStartX} ${bgStartY} A ${r} ${r} 0 ${largeArc} 1 ${fillEndX} ${fillEndY}`;

  // Color
  const color =
    risk_status === 'SAFE'
      ? 'var(--status-safe)'
      : risk_status === 'CAUTION'
      ? 'var(--status-caution)'
      : 'var(--status-danger)';

  const gradient =
    risk_status === 'SAFE'
      ? 'var(--gradient-safe)'
      : risk_status === 'CAUTION'
      ? 'var(--gradient-caution)'
      : 'var(--gradient-danger)';

  return (
    <div className="glass-card agent-card animate-fade-in-up" id="risk-meter-card">
      <div className="agent-card-header">
        <div className="agent-card-title-row">
          <div className="agent-card-icon" style={{ background: 'rgba(244, 63, 94, 0.15)' }}>🛡️</div>
          <span className="agent-card-title">Trust Score</span>
        </div>
        <span className={`agent-card-badge badge-${risk_status.toLowerCase()}`}>{risk_status}</span>
      </div>
      <div className="risk-meter-container">
        <svg className="risk-meter-svg" viewBox="0 20 200 100" id="risk-meter-gauge">
          <defs>
            <linearGradient id="meterGradient" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="var(--status-safe)" />
              <stop offset="50%" stopColor="var(--status-caution)" />
              <stop offset="100%" stopColor="var(--status-danger)" />
            </linearGradient>
          </defs>
          {/* Background arc */}
          <path
            d={bgPath}
            fill="none"
            stroke="rgba(255,255,255,0.06)"
            strokeWidth="12"
            strokeLinecap="round"
          />
          {/* Filled arc */}
          <path
            d={fillPath}
            fill="none"
            stroke="url(#meterGradient)"
            strokeWidth="12"
            strokeLinecap="round"
            style={{
              transition: 'all 1s cubic-bezier(0.4, 0, 0.2, 1)',
            }}
          />
          {/* Needle dot */}
          <circle
            cx={fillEndX}
            cy={fillEndY}
            r="6"
            fill={color}
            style={{
              filter: `drop-shadow(0 0 6px ${color})`,
              transition: 'all 1s cubic-bezier(0.4, 0, 0.2, 1)',
            }}
          />
        </svg>
        <div className="risk-meter-value" style={{ color }} id="risk-score-value">
          {risk_score}
        </div>
        <div className="risk-meter-label" style={{ color }}>
          {risk_status === 'SAFE' ? 'LOW RISK' : risk_status === 'CAUTION' ? 'MODERATE RISK' : 'HIGH RISK'}
        </div>
      </div>
      {risk_flags && risk_flags.length > 0 && (
        <div className="risk-flags">
          {risk_flags.map((flag, i) => (
            <div className="risk-flag" key={i}>
              <span className="risk-flag-icon">
                {risk_status === 'DANGER' ? '🔴' : risk_status === 'CAUTION' ? '🟡' : '🟢'}
              </span>
              {flag}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
