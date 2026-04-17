from typing import List, Optional
from ..models.schemas import RiskProduct, AnalyzedProduct

class TrustAgent:
    def __init__(self) -> None:
        pass

    def _calculate_market_avg(self, products: List[AnalyzedProduct]) -> Optional[float]:
        prices = [p.price for p in products if p.price > 0]
        if not prices:
            return None
        return sum(prices) / len(prices)

    def _detect_price_anomaly(self, product: AnalyzedProduct, market_avg: Optional[float]) -> tuple[int, str]:
        if market_avg is None or product.price <= 0:
            return 0, ""
        ratio = product.price / market_avg
        if ratio < 0.6:
            return 35, f"Price ${product.price:.2f} is {int((1-ratio)*100)}% below market average ${market_avg:.2f}. Suspicious."
        if ratio < 0.75:
            return 20, f"Price ${product.price:.2f} is significantly below market average."
        return 0, ""

    def score_products(self, products: List[AnalyzedProduct]) -> List[RiskProduct]:
        risk_products = []
        market_avg = self._calculate_market_avg(products)

        for product in products:
            risk_score = 0
            flags = []

            price_penalty, price_flag = self._detect_price_anomaly(product, market_avg)
            if price_penalty > 0:
                risk_score += price_penalty
                flags.append(price_flag)

            if product.price <= 0:
                risk_score += 50
                flags.append("Missing or invalid price data.")

            if "refurb" in product.name.lower() or "refurb" in product.seller.lower():
                risk_score += 20
                flags.append("Refurbished or secondhand offer detected.")

            if any(term in product.name.lower() for term in ["old stock", "clearance", "scratch", "used", "damaged"]):
                risk_score += 20
                flags.append("Product appears to be discounted or clearance item.")

            if "new seller" in product.seller.lower() or len(product.seller) < 5:
                risk_score += 20
                flags.append("Seller appears to be new or low-profile.")

            if "no return" in product.name.lower() or "no return" in product.seller.lower():
                risk_score += 15
                flags.append("No return policy detected.")

            if product.score >= 75:
                risk_score -= 10
                flags.append("Strong value score reduces overall risk.")

            risk_score = max(0, min(100, risk_score))
            if risk_score < 30:
                status = "SAFE"
            elif risk_score < 60:
                status = "CAUTION"
            else:
                status = "DANGER"

            market_avg_text = f"${market_avg:.2f}" if market_avg is not None else "N/A"
            reasoning = (
                f"Risk assessment: {risk_score}/100 → {status}. "
                f"Market avg: {market_avg_text}. "
                f"Product verdict: {product.verdict}."
            )

            if not flags:
                flags.append("No obvious risk flags detected.")

            risk_products.append(
                RiskProduct(
                    name=product.name,
                    price=product.price,
                    url=product.url,
                    seller=product.seller,
                    image_url=product.image_url,
                    source=product.source,
                    score=product.score,
                    verdict=product.verdict,
                    reasoning=product.reasoning,
                    risk_score=risk_score,
                    risk_status=status,
                    risk_flags=flags,
                    risk_reasoning=reasoning,
                )
            )

        return risk_products
