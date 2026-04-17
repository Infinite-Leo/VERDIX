import json
import os
from uuid import uuid4
from typing import Optional
from ..locus.client import LocusClient
from ..locus.config import TRANSACTION_LOG_PATH, MAX_TRANSACTION_USDC, SPENDING_LIMIT_USDC
from ..models.schemas import ExecutorResult, NegotiationResult, RiskProduct, RunRequest

class ExecutorAgent:
    def __init__(self, client: LocusClient) -> None:
        self.client = client
        self.log_path = os.path.abspath(TRANSACTION_LOG_PATH)
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
        if not os.path.exists(self.log_path):
            with open(self.log_path, "w", encoding="utf-8") as file:
                json.dump([], file)

    async def execute(
        self,
        product: Optional[RiskProduct],
        negotiation: NegotiationResult,
        request: RunRequest,
        memory: object,
    ) -> ExecutorResult:
        balance_info = await self.client.get_balance()
        wallet_balance = balance_info.get("balance", 0.0)
        wallet_cost = balance_info.get("cost", 0.0)

        if not product:
            return ExecutorResult(
                status="REFUSED",
                reason="❌ No safe or valuable product found. VERDIX refuses to purchase without a verified target.",
                wallet_balance=wallet_balance,
                wallet_cost=wallet_cost,
            )

        final_price = negotiation.final_price if negotiation else product.price
        if final_price <= 0:
            final_price = product.price

        if product.verdict == "REJECT":
            return ExecutorResult(
                status="REFUSED",
                reason=f"❌ Analyst rejected '{product.name}' with score {product.score}/100. Reason: {product.reasoning[:100]}",
                product=product,
                final_price=final_price,
                wallet_balance=wallet_balance,
                wallet_cost=wallet_cost,
            )

        if product.risk_status == "DANGER":
            return ExecutorResult(
                status="REFUSED",
                reason=f"❌ Risk score {product.risk_score}/100 is too high for autonomous execution. Flags: {', '.join(product.risk_flags[:3])}",
                product=product,
                final_price=final_price,
                wallet_balance=wallet_balance,
                wallet_cost=wallet_cost,
            )

        if request.budget and final_price > request.budget:
            return ExecutorResult(
                status="REFUSED",
                reason=f"❌ Final price ${final_price:.2f} exceeds user budget ${request.budget:.2f}. VERDIX respects spending limits.",
                product=product,
                final_price=final_price,
                wallet_balance=wallet_balance,
                wallet_cost=wallet_cost,
            )

        if final_price > wallet_balance:
            return ExecutorResult(
                status="REFUSED",
                reason=f"❌ Wallet balance (${wallet_balance:.2f} USDC) is insufficient for the negotiated price (${final_price:.2f}).",
                product=product,
                final_price=final_price,
                wallet_balance=wallet_balance,
                wallet_cost=wallet_cost,
            )

        if final_price > MAX_TRANSACTION_USDC or final_price > SPENDING_LIMIT_USDC:
            return ExecutorResult(
                status="REFUSED",
                reason=f"❌ The negotiated price (${final_price:.2f}) exceeds the configured spending limit (${MAX_TRANSACTION_USDC} USDC).",
                product=product,
                final_price=final_price,
                wallet_balance=wallet_balance,
                wallet_cost=wallet_cost,
            )

        if product.risk_status == "CAUTION" and final_price > 50:
            return ExecutorResult(
                status="REFUSED",
                reason=f"⚠️ Product flagged with CAUTION (risk {product.risk_score}/100). Requires manual approval for purchases over $50.",
                product=product,
                final_price=final_price,
                wallet_balance=wallet_balance,
                wallet_cost=wallet_cost,
            )

        tx_id = f"tx_{uuid4().hex[:12]}"
        record = {
            "tx_id": tx_id,
            "product": product.name,
            "price": final_price,
            "seller": product.seller,
            "status": "PURCHASED",
            "personality": request.personality,
        }

        try:
            with open(self.log_path, "r+", encoding="utf-8") as file:
                data = json.load(file)
                if not isinstance(data, list):
                    data = []
                data.append(record)
                file.seek(0)
                json.dump(data, file, indent=2)
                file.truncate()
        except Exception:
            pass

        return ExecutorResult(
            status="PURCHASED",
            reason=f"✅ Purchase executed successfully. {product.name} at ${final_price:.2f} from {product.seller}.",
            product=product,
            final_price=final_price,
            tx_id=tx_id,
            wallet_balance=wallet_balance,
            wallet_cost=wallet_cost,
        )
