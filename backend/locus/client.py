import json
import logging
import re
from typing import Any, Dict, List, Optional
import httpx
from .config import LOCUS_API_KEY, LOCUS_BASE_URL, LOCUS_AI_MODEL, DEMO_MODE
from . import demo_data

logger = logging.getLogger("verdix.locus")


class LocusClient:
    def __init__(self) -> None:
        self.base_url = LOCUS_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {LOCUS_API_KEY}",
            "Content-Type": "application/json",
        }
        self.client = httpx.AsyncClient(timeout=30.0)
        self._demo_mode = DEMO_MODE
        self._live_available: Optional[bool] = None  # cached after first check

    @property
    def is_demo(self) -> bool:
        return self._demo_mode

    async def _check_live(self) -> bool:
        """Check if live Locus APIs are available (wallet has funds)."""
        if self._live_available is not None:
            return self._live_available
        try:
            response = await self.client.get(
                f"{self.base_url}/pay/balance", headers=self.headers
            )
            response.raise_for_status()
            body = response.json()
            data = body.get("data", body) if isinstance(body, dict) else {}
            balance = float(data.get("usdc_balance", 0) if isinstance(data, dict) else 0)
            self._live_available = balance > 0.01
            if not self._live_available:
                logger.info("Locus wallet empty — using demo mode")
            else:
                logger.info(f"Locus wallet funded (${balance:.2f}) — using live APIs")
            return self._live_available
        except Exception:
            self._live_available = False
            logger.info("Cannot reach Locus API — using demo mode")
            return False

    async def _parse_cost(self, response: httpx.Response) -> float:
        header = response.headers.get("x-locus-cost") or response.headers.get("x-usdc-cost")
        if header:
            try:
                return float(header)
            except ValueError:
                pass

        try:
            body = response.json()
            if isinstance(body, dict):
                cost = body.get("cost") or body.get("usd_cost") or body.get("pricing")
                if cost is not None:
                    return float(cost)
        except Exception:
            pass

        return 0.0

    async def search(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        if self._demo_mode and not await self._check_live():
            return await demo_data.demo_search(query, num_results)

        payload = {"query": query, "numResults": num_results}
        response = await self.client.post(
            f"{self.base_url}/wrapped/exa/search", json=payload, headers=self.headers
        )
        response.raise_for_status()
        body = response.json()
        data = body.get("data", body) if isinstance(body, dict) else body
        return {"data": data, "cost": await self._parse_cost(response)}

    async def scrape(self, url: str) -> Dict[str, Any]:
        if self._demo_mode and not await self._check_live():
            return {"data": {}, "cost": 0.0}

        payload = {"url": url}
        response = await self.client.post(
            f"{self.base_url}/wrapped/firecrawl/scrape", json=payload, headers=self.headers
        )
        response.raise_for_status()
        body = response.json()
        data = body.get("data", body) if isinstance(body, dict) else body
        return {"data": data, "cost": await self._parse_cost(response)}

    async def ai_chat(
        self,
        system: str,
        user: str,
        model: str = LOCUS_AI_MODEL,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if self._demo_mode and not await self._check_live():
            return await demo_data.demo_ai_chat(system, user, model, params)

        payload: Dict[str, Any] = {
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }
        if params:
            payload["params"] = params

        response = await self.client.post(
            f"{self.base_url}/wrapped/openai/chat", json=payload, headers=self.headers
        )
        response.raise_for_status()
        body = response.json()

        # Unwrap Locus envelope: { success: true, data: { choices: [...] } }
        inner = body
        if isinstance(body, dict) and "data" in body:
            inner = body["data"] if isinstance(body["data"], dict) else body

        output = ""
        if isinstance(inner, dict):
            output = inner.get("output") or "".join(
                choice.get("message", {}).get("content", "")
                for choice in inner.get("choices", [])
                if isinstance(choice, dict)
            )
            if not output and isinstance(inner.get("choices"), list) and inner["choices"]:
                first = inner["choices"][0]
                output = first.get("message", {}).get("content", "") if isinstance(first, dict) else ""

        return {"output": output.strip(), "cost": await self._parse_cost(response)}

    async def get_balance(self) -> Dict[str, Any]:
        if self._demo_mode and not await self._check_live():
            return await demo_data.demo_balance()

        response = await self.client.get(f"{self.base_url}/pay/balance", headers=self.headers)
        response.raise_for_status()
        body = response.json()
        data = body.get("data", body) if isinstance(body, dict) else {}
        balance = 0.0
        if isinstance(data, dict):
            balance = float(data.get("usdc_balance", 0) or data.get("balance", 0) or 0)
        return {"data": body, "cost": await self._parse_cost(response), "balance": balance}

    async def get_status(self) -> Dict[str, Any]:
        response = await self.client.get(f"{self.base_url}/status", headers=self.headers)
        response.raise_for_status()
        return {"data": response.json(), "cost": await self._parse_cost(response)}

    async def close(self) -> None:
        await self.client.aclose()
