from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field

class RunRequest(BaseModel):
    query: str
    budget: Optional[float] = None
    personality: str = Field(default="balanced", pattern="^(budget|balanced|premium)$")
    user_id: str = "default"

class Product(BaseModel):
    name: str
    price: float
    url: Optional[str] = None
    seller: str = "Unknown seller"
    image_url: Optional[str] = None
    source: str = "locus"

class ScoutResult(BaseModel):
    products: List[Product] = []
    search_cost: float = 0.0

class AnalyzedProduct(Product):
    score: int
    verdict: str
    reasoning: str

class RiskProduct(AnalyzedProduct):
    risk_score: int
    risk_status: str
    risk_flags: List[str]
    risk_reasoning: str

class NegotiationTurn(BaseModel):
    role: str
    message: str

class NegotiationResult(BaseModel):
    turns: List[NegotiationTurn]
    original_price: float
    final_price: float
    savings: float
    personality_used: str
    negotiation_cost: float = 0.0

class ExecutorResult(BaseModel):
    status: str
    reason: str
    product: Optional[Product] = None
    final_price: Optional[float] = None
    tx_id: Optional[str] = None
    wallet_balance: Optional[float] = None
    wallet_cost: float = 0.0

class ConflictReport(BaseModel):
    has_conflict: bool
    conflict_type: str
    description: str
    recommendation: str

class CostReport(BaseModel):
    search_cost: float = 0.0
    ai_reasoning_cost: float = 0.0
    negotiation_cost: float = 0.0
    wallet_cost: float = 0.0
    total: float = 0.0
    currency: str = "USDC"

    def add(self, cost_type: str, amount: float) -> None:
        if cost_type == "search":
            self.search_cost += amount
        elif cost_type == "ai":
            self.ai_reasoning_cost += amount
        elif cost_type == "negotiation":
            self.negotiation_cost += amount
        elif cost_type == "wallet":
            self.wallet_cost += amount
        self.total = self.search_cost + self.ai_reasoning_cost + self.negotiation_cost + self.wallet_cost

class PipelineResult(BaseModel):
    query: str
    budget: Optional[float]
    user_id: str
    products: List[RiskProduct]
    winner: Optional[RiskProduct]
    negotiation: Optional[NegotiationResult]
    execution: ExecutorResult
    conflict: ConflictReport
    cost: CostReport
    memory_used: Optional[dict] = None
    demo_mode: bool = False

