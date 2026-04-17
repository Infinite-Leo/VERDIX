'use client';

import { Personality } from '../types';

interface PersonalityBarProps {
  personality: Personality;
  onChange: (p: Personality) => void;
}

const modes: { key: Personality; label: string; icon: string }[] = [
  { key: 'budget', label: 'Budget', icon: '💰' },
  { key: 'balanced', label: 'Balanced', icon: '⚖️' },
  { key: 'premium', label: 'Premium', icon: '👑' },
];

export default function PersonalityBar({ personality, onChange }: PersonalityBarProps) {
  return (
    <div className="personality-selector" id="personality-selector">
      {modes.map((m) => (
        <button
          key={m.key}
          className={`personality-btn ${personality === m.key ? 'active' : ''}`}
          onClick={() => onChange(m.key)}
          aria-label={`Set personality to ${m.label}`}
          id={`personality-${m.key}`}
        >
          {m.icon} {m.label}
        </button>
      ))}
    </div>
  );
}
