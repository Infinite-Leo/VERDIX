from typing import List, Any, Dict
from ..locus.client import LocusClient
from ..models.schemas import Product, ScoutResult

class ScoutAgent:
    def __init__(self, client: LocusClient) -> None:
        self.client = client

    def _extract_results(self, data: Any) -> List[Dict]:
        """Extract results list from various API response formats."""
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            # Try common response structures
            if "results" in data:
                return data["results"] if isinstance(data["results"], list) else []
            if "data" in data:
                inner = data["data"]
                if isinstance(inner, list):
                    return inner
                if isinstance(inner, dict) and "results" in inner:
                    return inner["results"] if isinstance(inner["results"], list) else []
            if "items" in data:
                return data["items"] if isinstance(data["items"], list) else []
            if "products" in data:
                return data["products"] if isinstance(data["products"], list) else []
        return []

    async def search(self, query: str, limit: int = 5) -> ScoutResult:
        try:
            response = await self.client.search(query, num_results=limit)
            search_cost = response.get("cost", 0.0)
            data = response.get("data", {})
            results = self._extract_results(data)
            products = []
            for item in results:
                seller = item.get("seller")
                if isinstance(seller, dict):
                    seller_name = seller.get("name", "Unknown seller")
                else:
                    seller_name = seller or "Unknown seller"

                price = 0.0
                try:
                    price = float(item.get("price", 0.0) or 0.0)
                except (TypeError, ValueError):
                    price = 0.0

                products.append(
                    Product(
                        name=item.get("name") or item.get("title", "Unnamed product"),
                        price=price,
                        url=item.get("url"),
                        seller=seller_name,
                        image_url=item.get("image"),
                        source=item.get("source", "locus"),
                    )
                )

            return ScoutResult(products=products[:limit], search_cost=search_cost)
        except Exception:
            return ScoutResult(products=[], search_cost=0.0)

    async def enrich_price(self, product: Product) -> Product:
        if product.url and product.price <= 0:
            try:
                response = await self.client.scrape(product.url)
                data = response.get("data", {})
                price = float(data.get("price", product.price) or product.price)
                return product.model_copy(update={"price": price})
            except Exception:
                return product
        return product
