from typing import List, Optional
from .locus.client import LocusClient
from .agents.memory import MemoryAgent, UserMemory
from .agents.scout import ScoutAgent
from .agents.analyst import AnalystAgent
from .agents.trust import TrustAgent
from .agents.negotiator import NegotiatorAgent
from .agents.executor import ExecutorAgent
from .models.schemas import (
    RunRequest,
    PipelineResult,
    RiskProduct,
    NegotiationResult,
    ExecutorResult,
    ConflictReport,
    CostReport,
)

class VerdixOrchestrator:
    def __init__(self) -> None:
        self.client = LocusClient()
        self.memory_agent = MemoryAgent()
        self.scout = ScoutAgent(self.client)
        self.analyst = AnalystAgent()
        self.trust = TrustAgent()
        self.negotiator = NegotiatorAgent(self.client)
        self.executor = ExecutorAgent(self.client)

    async def run_pipeline(self, request: RunRequest) -> PipelineResult:
        memory = self.memory_agent.load_memory(request.user_id)
        
        scout_result = await self.scout.search(request.query, limit=5)
        products = scout_result.products
        
        analyzed = self.analyst.score_products(products, request.budget, memory)
        risk_products = self.trust.score_products(analyzed)
        conflict = self.detect_conflict(risk_products)

        winner = self.select_winner(risk_products)
        negotiation = None
        if winner and winner.verdict == "APPROVE":
            negotiation = await self.negotiator.negotiate(winner, request.personality, memory)
        else:
            negotiation = NegotiationResult(
                turns=[],
                original_price=winner.price if winner else 0.0,
                final_price=winner.price if winner else 0.0,
                savings=0.0,
                personality_used=request.personality,
            )

        execution = await self.executor.execute(winner, negotiation, request, memory)

        if execution.status == "PURCHASED" and execution.tx_id:
            self.memory_agent.record_transaction(execution.tx_id, winner.name, execution.final_price or winner.price)

        cost = CostReport(
            search_cost=scout_result.search_cost,
            ai_reasoning_cost=0.0,
            negotiation_cost=negotiation.negotiation_cost if negotiation else 0.0,
            wallet_cost=execution.wallet_cost,
            total=scout_result.search_cost + (negotiation.negotiation_cost if negotiation else 0.0) + execution.wallet_cost,
        )

        return PipelineResult(
            query=request.query,
            budget=request.budget,
            user_id=request.user_id,
            products=risk_products,
            winner=winner,
            negotiation=negotiation,
            execution=execution,
            conflict=conflict,
            cost=cost,
            memory_used=memory.model_dump(),
            demo_mode=self.client.is_demo,
        )

    def select_winner(self, risk_products: List[RiskProduct]) -> Optional[RiskProduct]:
        approved = [product for product in risk_products if product.verdict == "APPROVE"]
        if not approved:
            return None
        approved.sort(key=lambda item: (item.risk_score, -item.score, item.price))
        return approved[0]

    def detect_conflict(self, risk_products: List[RiskProduct]) -> ConflictReport:
        if not risk_products:
            return ConflictReport(
                has_conflict=False,
                conflict_type="NONE",
                description="No products available to analyze.",
                recommendation="Please refine the query or budget.",
            )

        approved = [p for p in risk_products if p.verdict == "APPROVE"]
        if not approved:
            return ConflictReport(
                has_conflict=True,
                conflict_type="NO_APPROVED_PRODUCTS",
                description="All products were rejected by the Analyst agent based on value scoring.",
                recommendation="Increase your budget or broaden your search criteria.",
            )

        dangers = [p for p in risk_products if p.risk_status == "DANGER"]
        if dangers:
            danger_product = dangers[0]
            approved_danger = next((p for p in approved if p.name == danger_product.name), None)
            if approved_danger:
                return ConflictReport(
                    has_conflict=True,
                    conflict_type="VALUE_VS_RISK",
                    description=(
                        f"⚠️ CONFLICT: '{approved_danger.name}' has good value "
                        f"but Trust agent flags DANGER (risk {danger_product.risk_score}/100). "
                        f"Flags: {', '.join(danger_product.risk_flags[:2])}"
                    ),
                    recommendation="Review the risk flags or choose a safer alternative.",
                )

        return ConflictReport(
            has_conflict=False,
            conflict_type="NONE",
            description="Agents are aligned on candidate products.",
            recommendation="Proceed with evaluation.",
        )
