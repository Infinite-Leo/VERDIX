// Type definitions for VERDIX frontend

export type Personality = 'budget' | 'balanced' | 'premium';

export interface Product {
  name: string;
  price: number;
  url?: string;
  seller: string;
  image_url?: string;
  source: string;
}

export interface RiskProduct extends Product {
  score: number;
  verdict: string;
  reasoning: string;
  risk_score: number;
  risk_status: string;
  risk_flags: string[];
  risk_reasoning: string;
}

export interface NegotiationTurn {
  role: string;
  message: string;
}

export interface NegotiationResult {
  turns: NegotiationTurn[];
  original_price: number;
  final_price: number;
  savings: number;
  personality_used: string;
  negotiation_cost: number;
}

export interface ExecutorResult {
  status: string;
  reason: string;
  product?: Product;
  final_price?: number;
  tx_id?: string;
  wallet_balance?: number;
  wallet_cost: number;
}

export interface ConflictReport {
  has_conflict: boolean;
  conflict_type: string;
  description: string;
  recommendation: string;
}

export interface CostReport {
  search_cost: number;
  ai_reasoning_cost: number;
  negotiation_cost: number;
  wallet_cost: number;
  total: number;
  currency: string;
}

export interface PipelineResult {
  query: string;
  budget?: number;
  user_id: string;
  products: RiskProduct[];
  winner?: RiskProduct;
  negotiation?: NegotiationResult;
  execution: ExecutorResult;
  conflict: ConflictReport;
  cost: CostReport;
  memory_used?: Record<string, unknown>;
  demo_mode?: boolean;
}

export type AgentStep = 
  | 'idle'
  | 'scout'
  | 'analyst'
  | 'trust'
  | 'negotiator'
  | 'executor'
  | 'done'
  | 'error';
