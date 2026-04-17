import re
from typing import List
from ..locus.client import LocusClient
from ..agents.memory import UserMemory
from ..models.schemas import NegotiationResult, NegotiationTurn, RiskProduct

class NegotiatorAgent:
    def __init__(self, client: LocusClient) -> None:
        self.client = client

    @staticmethod
    def _parse_price(text: str, fallback: float) -> float:
        matches = re.findall(r"\b\d+[\.,]?\d*\b", text.replace("₹", ""))
        prices = [float(m.replace(",", "")) for m in matches if float(m.replace(",", "")) > 0]
        if prices:
            return min(prices)
        return fallback

    def _build_buyer_prompt(self, product: RiskProduct, personality: str, memory: UserMemory) -> str:
        safe_hints = ", ".join(memory.preferences[:3]) if memory.preferences else ""
        target = product.price * (0.8 if personality == "budget" else 0.9 if personality == "balanced" else 0.95)
        return (
            f"You are a {personality} buyer negotiating on a product named '{product.name}' priced at ₹{product.price:.2f}. "
            f"Your goal is to get a better deal while maintaining a realistic tone. "
            f"Use prior customer preferences: {safe_hints}. "
            f"Start with an opening offer near ₹{target:.2f} and mention that you are a returning customer."
        )

    def _build_seller_prompt(self, product: RiskProduct, mode: str) -> str:
        return (
            f"You are a seller representing '{product.name}'. The buyer has requested a better price for a returning customer. "
            f"Keep the reply realistic and reflect the seller's personality as a responsive negotiator. "
            f"If the mode is budget, be firm but fair. If balanced, be cooperative. If premium, offer bundles or added value."
        )

    async def negotiate(
        self,
        product: RiskProduct,
        personality: str,
        memory: UserMemory,
    ) -> NegotiationResult:
        if product is None:
            return NegotiationResult(turns=[], original_price=0.0, final_price=0.0, savings=0.0, personality_used=personality)

        buyer_prompt = self._build_buyer_prompt(product, personality, memory)
        seller_prompt = self._build_seller_prompt(product, personality)

        seller_response = await self.client.ai_chat(
            system=seller_prompt,
            user=buyer_prompt,
            params={"mode": personality},
        )
        buyer_response = await self.client.ai_chat(
            system=f"You are a {personality} buyer responding to the seller.",
            user=seller_response["output"],
            params={"original_price": product.price},
        )

        seller_turn = NegotiationTurn(role="seller", message=seller_response["output"])
        buyer_turn = NegotiationTurn(role="buyer", message=buyer_response["output"])
        final_price = self._parse_price(buyer_response["output"], product.price)
        savings = max(0.0, product.price - final_price)
        negotiation_cost = seller_response.get("cost", 0.0) + buyer_response.get("cost", 0.0)

        return NegotiationResult(
            turns=[seller_turn, buyer_turn],
            original_price=product.price,
            final_price=final_price,
            savings=savings,
            personality_used=personality,
            negotiation_cost=negotiation_cost,
        )
