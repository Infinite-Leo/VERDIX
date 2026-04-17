from typing import List, Optional
from .memory import UserMemory
from ..models.schemas import AnalyzedProduct, Product

class AnalystAgent:
    def __init__(self) -> None:
        pass

    def score_products(
        self,
        products: List[Product],
        budget: Optional[float],
        memory: UserMemory,
    ) -> List[AnalyzedProduct]:
        scored = []
        preferences = [pref.lower() for pref in memory.preferences]
        avoid_terms = [term.lower() for term in memory.avoid]

        for product in products:
            brand_bonus = 0
            avoid_penalty = 0
            memory_reason = []

            low_price = budget and budget > 0 and product.price <= budget
            if low_price:
                brand_bonus += 10
                memory_reason.append("The item fits the user budget.")

            if any(pref in product.name.lower() for pref in preferences):
                brand_bonus += 15
                memory_reason.append("Matches a past preferred brand or category.")

            if any(term in product.name.lower() or term in product.seller.lower() for term in avoid_terms):
                avoid_penalty += 25
                memory_reason.append("Includes a term from the user's avoid list.")

            price_score = 50
            if budget and budget > 0:
                ratio = product.price / budget
                if ratio <= 1.0:
                    # Within budget: score 40-70 based on how much under budget
                    price_score = int(40 + (1 - ratio) * 30)
                else:
                    # Over budget: penalize proportionally
                    price_score = max(5, int(40 - (ratio - 1.0) * 100))

            score = max(0, min(100, price_score + brand_bonus - avoid_penalty))
            verdict = "APPROVE" if score >= 40 else "REJECT"
            reasoning = (
                f"Base value score {price_score}, memory bonus +{brand_bonus}, penalty -{avoid_penalty}. "
                f"Final score {score}/100. "
            )
            if memory_reason:
                reasoning += "Memory influence: " + " ".join(memory_reason)

            if not memory_reason:
                reasoning += "No strong memory signals detected."

            scored.append(
                AnalyzedProduct(
                    name=product.name,
                    price=product.price,
                    url=product.url,
                    seller=product.seller,
                    image_url=product.image_url,
                    source=product.source,
                    score=score,
                    verdict=verdict,
                    reasoning=reasoning,
                )
            )

        return scored
