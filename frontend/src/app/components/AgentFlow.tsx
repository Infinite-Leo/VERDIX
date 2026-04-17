'use client';

import { AgentStep } from '../types';

interface AgentFlowProps {
  currentStep: AgentStep;
}

const steps: { key: AgentStep; label: string; icon: string }[] = [
  { key: 'scout', label: 'Scout', icon: '🔍' },
  { key: 'analyst', label: 'Analyst', icon: '📊' },
  { key: 'trust', label: 'Trust', icon: '🛡️' },
  { key: 'negotiator', label: 'Negotiator', icon: '🤝' },
  { key: 'executor', label: 'Executor', icon: '⚡' },
];

function getStepStatus(
  stepKey: AgentStep,
  currentStep: AgentStep
): 'pending' | 'active' | 'completed' | 'failed' {
  if (currentStep === 'idle') return 'pending';
  if (currentStep === 'error') return 'failed';

  const order = steps.map((s) => s.key);
  const currentIdx = order.indexOf(currentStep as AgentStep);
  const stepIdx = order.indexOf(stepKey);

  if (currentStep === 'done') return 'completed';
  if (stepIdx < currentIdx) return 'completed';
  if (stepIdx === currentIdx) return 'active';
  return 'pending';
}

export default function AgentFlow({ currentStep }: AgentFlowProps) {
  return (
    <div className="agent-flow" id="agent-flow">
      {steps.map((step, i) => {
        const status = getStepStatus(step.key, currentStep);
        return (
          <div key={step.key} style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <div
              className={`flow-step ${status === 'active' ? 'active' : ''} ${
                status === 'completed' ? 'completed' : ''
              } ${status === 'failed' ? 'failed' : ''}`}
              id={`flow-step-${step.key}`}
            >
              <span className="flow-step-icon">
                {status === 'completed' ? '✓' : status === 'failed' ? '✗' : step.icon}
              </span>
              {step.label}
            </div>
            {i < steps.length - 1 && <span className="flow-arrow">→</span>}
          </div>
        );
      })}
    </div>
  );
}
